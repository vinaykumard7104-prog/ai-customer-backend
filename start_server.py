#!/usr/bin/env python3
"""
Quick server start script
IMPORTANT: Runs on 0.0.0.0 so Android can connect!
"""

import subprocess
import sys
import socket

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to detect"

local_ip = get_local_ip()

print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          InsightFlow AI Backend Server                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

✅ Starting server on http://0.0.0.0:8000
   (This allows Android devices to connect)

📱 Connect from Android:
   ┌─────────────────────────────────────────────────┐
   │ Emulator:  http://10.0.2.2:8000/              │
   │ Real Phone: http://{:<15}:8000/              │
   └─────────────────────────────────────────────────┘

🔐 Test Credentials:
   Email: admin@insightflow.ai
   Password: admin123

📚 API Documentation: 
   http://localhost:8000/docs

⚠️  IMPORTANT:
   • Make sure firewall allows port 8000
   • For real phone: phone and computer on same WiFi
   • Update RetrofitClient.kt with correct URL

Press Ctrl+C to stop the server
════════════════════════════════════════════════════════════
""".format(local_ip))

try:
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app:app", 
        "--reload", 
        "--host", "0.0.0.0",  # CRITICAL: Use 0.0.0.0 not localhost!
        "--port", "8000"
    ])
except KeyboardInterrupt:
    print("\n\n👋 Server stopped. Goodbye!")

