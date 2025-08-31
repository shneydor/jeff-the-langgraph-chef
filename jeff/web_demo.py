"""Launch script for Jeff's web demonstration interface."""

import uvicorn
from .web.app import app


def main():
    """Launch the web demo interface."""
    print("🍅 Starting Jeff the LangGraph Chef Web Demo...")
    print("🌐 Web interface will be available at: http://localhost:3000")
    print("📱 Mobile responsive design included")
    print("⚡ Real-time WebSocket communication enabled")
    print("🎭 Interactive demonstration features ready")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=3000,
        log_level="info",
        reload=False
    )


if __name__ == "__main__":
    main()