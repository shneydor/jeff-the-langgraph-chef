#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_demo_page():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>Jeff Test</title>
</head>
<body>
    <h1>🍅 Jeff Test Page</h1>
    <p>If you can see this, the server is working!</p>
    <button onclick="alert('Hello from Jeff!')">Test Button</button>
</body>
</html>
    """)

if __name__ == "__main__":
    import uvicorn
    print("🍅 Starting minimal Jeff server on http://localhost:8888")
    uvicorn.run(app, host="0.0.0.0", port=8888)