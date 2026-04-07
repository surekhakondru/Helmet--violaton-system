"""Flask application - Helmet Violation Detection API."""
import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

from config.settings import config
from utils.plate_utils import normalize_for_storage, plate_match_variants
from models.database import (
    get_mysql_session, get_mongodb_client, Violation, VehicleOwner,
    init_mysql, save_violation_json
)
from services.helmet_detector import HelmetDetector
from services.anpr import ANPR
from services.notifications import NotificationService
from services.vehicle_registry import VehicleRegistry
from services.analytics import AnalyticsService

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


@app.before_request
def log_request():
    logger.info(f"[{request.method}] {request.path} from {request.remote_addr}")

# Ensure directories exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(config.VIOLATIONS_FOLDER, exist_ok=True)
os.makedirs(config.JSON_EXPORT_FOLDER, exist_ok=True)

# Initialize services
helmet_detector = HelmetDetector()
anpr = ANPR()
notifier = NotificationService()
registry = VehicleRegistry()
analytics = AnalyticsService()

# Initialize database (SQLite by default)
if config.DATABASE_TYPE in ('sqlite', 'mysql'):
    init_mysql()


def _save_violation_db(vehicle_number: str, camera_location: str, image_path: str,
                       owner_name=None, owner_phone=None, owner_address=None,
                       violation_reason: str = 'No helmet') -> dict:
    """Save violation to database with reason."""
    violation_data = {
        'vehicle_number': vehicle_number,
        'violation_date': datetime.utcnow(),
        'violation_reason': violation_reason,
        'camera_location': camera_location,
        'image_path': image_path,
        'fine_amount': 400,
        'status': 'pending',
        'owner_name': owner_name,
        'owner_phone': owner_phone,
        'owner_address': owner_address,
    }
    
    if config.DATABASE_TYPE in ('sqlite', 'mysql'):
        try:
            session = get_mysql_session()
            v = Violation(**violation_data)
            session.add(v)
            session.commit()
            vid = v.id
            session.close()
            violation_data['id'] = vid
            violation_data['created_at'] = datetime.utcnow()
        except Exception as e:
            return {'error': str(e)}
    elif config.DATABASE_TYPE == 'mongodb':
        try:
            client = get_mongodb_client()
            db = client[config.MONGODB_URI.split('/')[-1].split('?')[0]]
            violation_data['violation_date'] = datetime.utcnow()
            result = db['violations'].insert_one(violation_data)
            violation_data['id'] = str(result.inserted_id)
            violation_data['created_at'] = datetime.utcnow()
        except Exception as e:
            return {'error': str(e)}
    
    # Save JSON record
    export_data = {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in violation_data.items()}
    save_violation_json(export_data, config.JSON_EXPORT_FOLDER)
    
    return violation_data


def _enrich_violation_from_registry(row: dict) -> dict:
    """
    If violation was saved before owner registration or lookup failed at detect time,
    attach owner details from vehicle_owners using the same plate normalization.
    """
    vn = (row.get('vehicle_number') or '').strip()
    if not vn or vn.upper() == 'UNKNOWN':
        return row
    if (row.get('owner_name') or '').strip():
        return row
    owner = registry.lookup_owner(vn)
    if not owner:
        return row
    out = {**row}
    out['owner_name'] = owner.get('owner_name')
    out['owner_phone'] = owner.get('phone_number')
    out['owner_address'] = owner.get('address')
    return out


def _backfill_violation_owner_sql(violation_id: int, owner: dict) -> None:
    """Persist owner on violation row so exports and offline reads stay consistent."""
    if not violation_id or not owner:
        return
    try:
        session = get_mysql_session()
        v = session.query(Violation).get(int(violation_id))
        if v and not (v.owner_name or '').strip():
            v.owner_name = owner.get('owner_name')
            v.owner_phone = owner.get('phone_number')
            v.owner_address = owner.get('address') or ''
            session.commit()
        session.close()
    except Exception as e:
        logger.warning('Backfill violation owner (SQL): %s', e)


def _backfill_violation_owner_mongo(doc_id: str, owner: dict) -> None:
    if not doc_id or not owner:
        return
    try:
        from bson import ObjectId
        client = get_mongodb_client()
        db = client[config.MONGODB_URI.split('/')[-1].split('?')[0]]
        db['violations'].update_one(
            {'_id': ObjectId(doc_id)},
            {'$set': {
                'owner_name': owner.get('owner_name'),
                'owner_phone': owner.get('phone_number'),
                'owner_address': owner.get('address') or '',
            }},
        )
    except Exception as e:
        logger.warning('Backfill violation owner (Mongo): %s', e)


# ============ API Routes ============

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'helmet-violation-api',
        'status': 'ok',
        'health': '/api/health',
        'docs': 'Use /api/health for health check'
    })

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    logger.info("Health check OK")
    return jsonify({'status': 'ok', 'service': 'helmet-violation-api'})


@app.route('/api/detect', methods=['POST'])
def detect_violation():
    """
    Process video frame - detect helmet violations and extract plate.
    Expects: multipart form with 'image' file and optional 'camera_location'.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    camera_location = request.form.get('camera_location', 'Unknown')
    static_vehicle = normalize_for_storage(request.form.get('vehicle_number', '') or '')  # Optional override
    
    import cv2
    import numpy as np
    from PIL import Image, ImageOps
    
    img = Image.open(file.stream)
    img = ImageOps.exif_transpose(img)  # Fix mobile photo orientation
    img = img.convert('RGB')
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Always detect helmet status for accurate UI display.
    helmet_result = helmet_detector.detect_helmet_status(frame, confidence_threshold=0.25)
    violations = helmet_result.get('without_detections', [])
    logger.info(f"Helmet status: {helmet_result.get('helmet_status')} (violations={len(violations)})")

    # Always run OCR for vehicle number display (even if helmet is present).
    vehicle_number = static_vehicle if static_vehicle else None
    if not vehicle_number:
        best_bbox = helmet_result.get('best_bbox')
        vehicle_number = anpr.read_plate(frame, best_bbox) if best_bbox else None
        if not vehicle_number:
            vehicle_number = anpr.read_plate(frame)
        if not vehicle_number:
            vehicle_number = 'UNKNOWN'
    vehicle_number = normalize_for_storage(vehicle_number)

    if violations:
        # Save evidence image (debug/evidence)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        img_filename = f"violation_{vehicle_number}_{timestamp}.jpg"
        img_path = os.path.join(config.VIOLATIONS_FOLDER, img_filename)
        annotated = helmet_detector.draw_helmet_status(frame.copy(), helmet_result)
        cv2.imwrite(img_path, annotated)

        # Lookup owner
        owner = registry.lookup_owner(vehicle_number)
        owner_name = owner.get('owner_name') if owner else None
        owner_phone = owner.get('phone_number') if owner else None
        owner_address = owner.get('address') if owner else None

        # Save to database with violation reason
        result = _save_violation_db(
            vehicle_number, camera_location, img_path,
            owner_name, owner_phone, owner_address,
            violation_reason='No helmet'
        )

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        # Auto-send notification if owner phone available
        if owner and owner.get('phone_number'):
            notif_result = notifier.send_both(
                owner['phone_number'],
                vehicle_number,
                result.get('fine_amount', 500),
                camera_location
            )
            result['notification_sent'] = notif_result

        return jsonify({
            'violation_detected': True,
            'vehicle_number': vehicle_number,
            'helmet_present': helmet_result.get('helmet_present'),
            'helmet_status': helmet_result.get('helmet_status'),
            'helmet_confidence': helmet_result.get('helmet_confidence'),
            'helmet_without_count': len(helmet_result.get('without_detections', [])),
            'helmet_with_count': len(helmet_result.get('with_detections', [])),
            'violation': result,
            'owner': owner
        })

    # No violation: still return helmet + vehicle info for the UI.
    return jsonify({
        'violation_detected': False,
        'vehicle_number': vehicle_number,
        'helmet_present': helmet_result.get('helmet_present'),
        'helmet_status': helmet_result.get('helmet_status'),
        'helmet_confidence': helmet_result.get('helmet_confidence'),
        'helmet_without_count': len(helmet_result.get('without_detections', [])),
        'helmet_with_count': len(helmet_result.get('with_detections', [])),
        'message': f"Helmet status: {helmet_result.get('helmet_status')}",
    })


@app.route('/api/violations', methods=['GET'])
def list_violations():
    """List violations with optional filters."""
    limit = min(int(request.args.get('limit', 50)), 100)
    offset = int(request.args.get('offset', 0))
    raw_plate = (request.args.get('vehicle_number') or '').strip()
    filter_variants = None
    if raw_plate:
        filter_variants = plate_match_variants(raw_plate)
        if not filter_variants:
            filter_variants = ['__NO_PLATE_MATCH__']

    if config.DATABASE_TYPE in ('sqlite', 'mysql'):
        try:
            session = get_mysql_session()
            q = session.query(Violation)
            if filter_variants is not None:
                q = q.filter(Violation.vehicle_number.in_(filter_variants))
            violations = q.order_by(Violation.violation_date.desc()).offset(offset).limit(limit).all()
            data = []
            for v in violations:
                d = v.to_dict()
                before = (d.get('owner_name') or '').strip()
                d = _enrich_violation_from_registry(d)
                if not before and (d.get('owner_name') or '').strip():
                    own = {
                        'owner_name': d.get('owner_name'),
                        'phone_number': d.get('owner_phone'),
                        'address': d.get('owner_address'),
                    }
                    _backfill_violation_owner_sql(d.get('id'), own)
                data.append(d)
            session.close()
            return jsonify({'violations': data})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif config.DATABASE_TYPE == 'mongodb':
        try:
            client = get_mongodb_client()
            db = client[config.MONGODB_URI.split('/')[-1].split('?')[0]]
            match = {'vehicle_number': {'$in': filter_variants}} if filter_variants is not None else {}
            data = list(db['violations'].find(match).sort('violation_date', -1).skip(offset).limit(limit))
            enriched = []
            for d in data:
                oid = str(d['_id'])
                d['_id'] = oid
                if 'violation_date' in d:
                    d['violation_date'] = d['violation_date'].isoformat()
                d['id'] = oid
                before = (d.get('owner_name') or '').strip()
                d = _enrich_violation_from_registry(d)
                if not before and (d.get('owner_name') or '').strip():
                    _backfill_violation_owner_mongo(oid, {
                        'owner_name': d.get('owner_name'),
                        'phone_number': d.get('owner_phone'),
                        'address': d.get('owner_address'),
                    })
                enriched.append(d)
            return jsonify({'violations': enriched})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'violations': []})


@app.route('/api/violations/<violation_id>', methods=['GET'])
def get_violation(violation_id):
    """Get single violation by ID."""
    if config.DATABASE_TYPE in ('sqlite', 'mysql'):
        try:
            session = get_mysql_session()
            v = session.query(Violation).get(int(violation_id))
            session.close()
            if v:
                d = v.to_dict()
                before = (d.get('owner_name') or '').strip()
                d = _enrich_violation_from_registry(d)
                if not before and (d.get('owner_name') or '').strip():
                    _backfill_violation_owner_sql(d.get('id'), {
                        'owner_name': d.get('owner_name'),
                        'phone_number': d.get('owner_phone'),
                        'address': d.get('owner_address'),
                    })
                return jsonify(d)
        except Exception:
            pass
    elif config.DATABASE_TYPE == 'mongodb':
        try:
            from bson import ObjectId
            client = get_mongodb_client()
            db = client[config.MONGODB_URI.split('/')[-1].split('?')[0]]
            v = db['violations'].find_one({'_id': ObjectId(violation_id)})
            if v:
                oid = str(v['_id'])
                v['_id'] = oid
                v['id'] = oid
                if 'violation_date' in v and hasattr(v['violation_date'], 'isoformat'):
                    v['violation_date'] = v['violation_date'].isoformat()
                before = (v.get('owner_name') or '').strip()
                v = _enrich_violation_from_registry(v)
                if not before and (v.get('owner_name') or '').strip():
                    _backfill_violation_owner_mongo(oid, {
                        'owner_name': v.get('owner_name'),
                        'phone_number': v.get('owner_phone'),
                        'address': v.get('owner_address'),
                    })
                return jsonify(v)
        except Exception:
            pass
    return jsonify({'error': 'Not found'}), 404


@app.route('/api/owner/lookup', methods=['GET'])
def lookup_owner():
    """Lookup vehicle owner by number plate."""
    vehicle_number = request.args.get('vehicle_number')
    if not vehicle_number:
        return jsonify({'error': 'vehicle_number required'}), 400
    
    owner = registry.lookup_owner(vehicle_number)
    if owner:
        return jsonify(owner)
    return jsonify({'error': 'Owner not found'}), 404


@app.route('/api/owner/register', methods=['POST'])
def register_owner():
    """Register vehicle owner."""
    data = request.get_json()
    if not data or not all(k in data for k in ['vehicle_number', 'owner_name', 'phone_number']):
        return jsonify({'error': 'vehicle_number, owner_name, phone_number required'}), 400
    
    ok = registry.register_owner(
        data['vehicle_number'],
        data['owner_name'],
        data['phone_number'],
        data.get('address', '')
    )
    if ok:
        return jsonify({'success': True})
    return jsonify({'error': 'Registration failed'}), 500


@app.route('/api/notify', methods=['POST'])
def send_notification():
    """Send SMS/WhatsApp notification for violation."""
    data = request.get_json()
    if not data or 'phone_number' not in data or 'vehicle_number' not in data:
        return jsonify({'error': 'phone_number and vehicle_number required'}), 400
    
    channel = data.get('channel', 'both')  # sms, whatsapp, both
    result = {}
    
    if channel in ['sms', 'both']:
        result['sms'] = notifier.send_sms(
            data['phone_number'],
            data['vehicle_number'],
            data.get('fine_amount', 500),
            data.get('camera_location', 'Unknown')
        )
    if channel in ['whatsapp', 'both']:
        result['whatsapp'] = notifier.send_whatsapp(
            data['phone_number'],
            data['vehicle_number'],
            data.get('fine_amount', 500),
            data.get('camera_location', 'Unknown')
        )
    
    return jsonify(result)


@app.route('/api/analytics/daily', methods=['GET'])
def analytics_daily():
    days = int(request.args.get('days', 7))
    return jsonify({'data': analytics.get_daily_violations(days)})


@app.route('/api/analytics/weekly', methods=['GET'])
def analytics_weekly():
    weeks = int(request.args.get('weeks', 4))
    return jsonify({'data': analytics.get_weekly_comparison(weeks)})


@app.route('/api/analytics/monthly', methods=['GET'])
def analytics_monthly():
    months = int(request.args.get('months', 6))
    return jsonify({'data': analytics.get_monthly_trends(months)})


@app.route('/api/analytics/summary', methods=['GET'])
def analytics_summary():
    return jsonify(analytics.get_summary())


@app.route('/api/violations/<violation_id>/image', methods=['GET'])
def get_violation_image(violation_id):
    """Serve violation evidence image."""
    if config.DATABASE_TYPE in ('sqlite', 'mysql'):
        session = get_mysql_session()
        v = session.query(Violation).get(int(violation_id))
        session.close()
        if v and v.image_path and os.path.exists(v.image_path):
            return send_file(v.image_path, mimetype='image/jpeg')
    return jsonify({'error': 'Image not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
