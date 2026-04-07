"""Entry point for Flask backend."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config.settings import config

if __name__ == '__main__':
    import socket
    port = int(os.getenv('FLASK_PORT', 5001))  # 5001 avoids Windows port 5000 conflict
    hostname = socket.gethostname()
    try:
        local_ip = [a for a in socket.gethostbyname_ex(hostname)[2] if not a.startswith('127.')][0]
    except Exception:
        local_ip = '127.0.0.1'
    print("=" * 50)
    print("Helmet Violation API")
    print("Local:   http://127.0.0.1:%d" % port)
    print("Network: http://%s:%d" % (local_ip, port))
    print("Mobile:  Use http://%s:%d in app Settings" % (local_ip, port))
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
