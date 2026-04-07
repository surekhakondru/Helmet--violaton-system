"""Process traffic camera video feed - detect violations and log them."""
import cv2
import requests
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.helmet_detector import HelmetDetector
from services.anpr import ANPR
from config.settings import config


def process_video_stream(video_source=0, api_url='http://localhost:5000', camera_location='Traffic Cam 1'):
    """
    Process video stream from camera or file.
    video_source: 0 for webcam, or path to video file
    """
    detector = HelmetDetector()
    anpr_reader = ANPR()
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("Error: Could not open video source")
        return
    
    frame_skip = 5  # Process every 5th frame for performance
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
        
        violations = detector.detect_violations(frame)
        
        if violations:
            vehicle_number = anpr_reader.read_plate(frame, violations[0]['bbox'])
            if not vehicle_number:
                vehicle_number = anpr_reader.read_plate(frame)
            if not vehicle_number:
                vehicle_number = 'UNKNOWN'
            
            # Save frame and send to API
            timestamp = __import__('datetime').datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            img_path = os.path.join(config.VIOLATIONS_FOLDER, f"violation_{vehicle_number}_{timestamp}.jpg")
            os.makedirs(config.VIOLATIONS_FOLDER, exist_ok=True)
            annotated = detector.draw_violations(frame.copy(), violations)
            cv2.imwrite(img_path, annotated)
            
            # POST to Flask API
            try:
                with open(img_path, 'rb') as f:
                    files = {'image': (os.path.basename(img_path), f, 'image/jpeg')}
                    data = {'camera_location': camera_location}
                    r = requests.post(f"{api_url}/api/detect", files=files, data=data)
                    if r.status_code == 200:
                        print(f"Violation logged: {vehicle_number}")
            except Exception as e:
                print(f"API error: {e}")
        
        # Display (optional)
        if frame_count % 10 == 0:
            cv2.imshow('Helmet Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default=0, help='Video source (0=webcam, or file path)')
    parser.add_argument('--api', default='http://localhost:5000', help='Flask API URL')
    parser.add_argument('--location', default='Traffic Cam 1', help='Camera location name')
    args = parser.parse_args()
    process_video_stream(int(args.source) if args.source.isdigit() else args.source, args.api, args.location)
