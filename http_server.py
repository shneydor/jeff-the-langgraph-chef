#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the directory containing our HTML file
os.chdir('/Users/shneydor/Documents/code/lectures/jeff-the-langgraph-chef')

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🍅 Jeff HTTP Server running at http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"🌐 Try: http://localhost:{PORT}/jeff_static.html")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")