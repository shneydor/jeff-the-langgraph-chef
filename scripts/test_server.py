#!/usr/bin/env python3

import threading
import time
import requests
from fastapi import FastAPI
import uvicorn

# Create simple app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def start_server():
    """Start server in a background thread"""
    uvicorn.run(app, host="127.0.0.1", port=9002, log_level="info")

if __name__ == "__main__":
    print("Starting server in background thread...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    print("Waiting for server to start...")
    time.sleep(3)
    
    print("Testing connection...")
    try:
        response = requests.get("http://127.0.0.1:9002/", timeout=5)
        print(f"✓ Success! Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
    
    print("Test complete.")