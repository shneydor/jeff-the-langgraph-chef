#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Create simple FastAPI app without lifespan
app = FastAPI(title="Jeff Simple Test")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def get_demo_page():
    """Serve a simple test page."""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jeff Simple Test</title>
    <style>body { font-family: Arial; text-align: center; padding: 50px; }</style>
</head>
<body>
    <h1>🍅 Jeff Simple Server Test</h1>
    <p>This is a simplified version without the complex lifespan manager.</p>
    <p>If you can see this, the basic server functionality works!</p>
    <button onclick="fetch('/test').then(r => r.text()).then(t => alert(t))">Test API</button>
</body>
</html>
    """)

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint."""
    return {"message": "Server is working!", "status": "ok"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("🍅 Starting Jeff Simple Server...")
    print("🌐 Available at: http://localhost:9000")
    uvicorn.run(app, host="0.0.0.0", port=9000, log_level="info")