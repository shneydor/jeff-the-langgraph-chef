#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
from pathlib import Path

# Change to the project root directory with error handling
try:
    project_root = Path(__file__).parent.parent
    if not project_root.exists():
        print(f"❌ Error: Project root directory not found: {project_root}")
        sys.exit(1)
    os.chdir(project_root)
except Exception as e:
    print(f"❌ Error setting up project directory: {e}")
    sys.exit(1)

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🍅 Jeff HTTP Server running at http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"🌐 Try: http://localhost:{PORT}/demo/jeff_static.html")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")