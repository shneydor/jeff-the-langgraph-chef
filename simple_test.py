#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Jeff's Simple Test Server</h1><p>If you see this, the server is working!</p>"

if __name__ == "__main__":
    print("Starting simple test server on http://127.0.0.1:8005")
    uvicorn.run(app, host="0.0.0.0", port=8005)