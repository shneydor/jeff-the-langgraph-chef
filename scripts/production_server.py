#!/usr/bin/env python3
"""Production server runner for Jeff the LangGraph Chef."""

import sys
import os
import signal
import uvicorn
from pathlib import Path

# Add project root to Python path
try:
    project_root = Path(__file__).parent.parent
    if not project_root.exists():
        print(f"❌ Error: Project root directory not found: {project_root}")
        sys.exit(1)
    sys.path.insert(0, str(project_root))
except Exception as e:
    print(f"❌ Error setting up project path: {e}")
    sys.exit(1)

from jeff.core.config import settings
from jeff.web.app import app
import structlog

# Configure logger
logger = structlog.get_logger()


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Shutdown signal received", signal=signum)
    sys.exit(0)


def main():
    """Run the production server with proper configuration."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Validate environment
    if not settings.anthropic_api_key:
        logger.error("ANTHROPIC_API_KEY is required but not set")
        sys.exit(1)
    
    # Production server configuration
    server_config = {
        "app": app,
        "host": settings.host,
        "port": settings.port,
        "log_level": settings.log_level.lower(),
        "access_log": True,
        "server_header": False,  # Security: don't expose server info
        "date_header": False,   # Security: don't expose date info
    }
    
    # Add development features only in debug mode
    if settings.debug:
        server_config.update({
            "reload": True,
            "reload_dirs": [str(project_root / "jeff")]
        })
    else:
        server_config.update({
            "workers": 1,  # Single worker for now, can scale later
            "limit_concurrency": 100,  # Limit concurrent connections
            "timeout_keep_alive": 30
        })
    
    logger.info(
        "Starting Jeff the LangGraph Chef production server",
        **{k: v for k, v in server_config.items() if k != "app"},
        environment=settings.env,
        debug_mode=settings.debug
    )
    
    print(f"""
🍅 Jeff the LangGraph Chef - Production Server
🌐 Server URL: http://{settings.host}:{settings.port}
📊 Health check: http://{settings.host}:{settings.port}/api/health
📈 Metrics: http://{settings.host}:{settings.port}/api/metrics
📚 API docs: http://{settings.host}:{settings.port}/docs
🔧 Environment: {settings.env}
🐛 Debug mode: {settings.debug}

Press Ctrl+C to stop the server
    """)
    
    try:
        uvicorn.run(**server_config)
    except Exception as e:
        logger.error("Server startup failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()