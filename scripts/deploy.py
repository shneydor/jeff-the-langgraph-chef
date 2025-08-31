#!/usr/bin/env python3
"""Deployment script for Jeff the LangGraph Chef."""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path


def run_command(command: str, description: str, check: bool = True) -> bool:
    """Run a command with logging."""
    print(f"🔄 {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=check
        )
        
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        
        print(f"✅ {description} completed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else 'Unknown error'}")
        return False


def check_prerequisites() -> bool:
    """Check deployment prerequisites."""
    print("🔍 Checking deployment prerequisites...")
    
    prerequisites = [
        ("docker", "Docker is required for containerized deployment"),
        ("docker-compose", "Docker Compose is required for orchestration")
    ]
    
    all_good = True
    for cmd, description in prerequisites:
        if subprocess.run(f"which {cmd}", shell=True, capture_output=True).returncode != 0:
            print(f"❌ {description}")
            all_good = False
        else:
            print(f"✅ {cmd} is available")
    
    return all_good


def deploy_local(env_file: str = None) -> bool:
    """Deploy locally with Docker Compose."""
    print("🚀 Starting local deployment...")
    
    # Check environment file
    if env_file and not Path(env_file).exists():
        print(f"❌ Environment file not found: {env_file}")
        return False
    
    # Build and start services
    commands = [
        ("docker-compose build", "Building Docker image"),
        ("docker-compose up -d", "Starting services"),
        ("docker-compose ps", "Checking service status")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            return False
    
    # Wait for services to be ready
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    # Health check
    return run_command(
        "curl -f http://localhost:8000/api/health", 
        "Health check",
        check=False
    )


def deploy_production() -> bool:
    """Deploy for production environment."""
    print("🏭 Starting production deployment...")
    
    # Set production environment variables
    env_vars = {
        "ENV": "production",
        "DEBUG": "false",
        "LOG_LEVEL": "WARNING"
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    return deploy_local()


def run_tests() -> bool:
    """Run integration tests."""
    print("🧪 Running integration tests...")
    
    test_commands = [
        ("python tests/test_integration.py", "Integration tests"),
        ("python tests/load_test.py", "Load tests")
    ]
    
    all_passed = True
    for cmd, desc in test_commands:
        if not run_command(cmd, desc, check=False):
            all_passed = False
    
    return all_passed


def main():
    """Main deployment orchestrator."""
    parser = argparse.ArgumentParser(description="Deploy Jeff the LangGraph Chef")
    parser.add_argument("--environment", choices=["local", "production"], default="local",
                       help="Deployment environment")
    parser.add_argument("--env-file", help="Environment file path")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-build", action="store_true", help="Skip building images")
    
    args = parser.parse_args()
    
    print("🍅 Jeff the LangGraph Chef - Deployment Script")
    print(f"🎯 Environment: {args.environment}")
    print("="*50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please install required tools.")
        sys.exit(1)
    
    # Deploy based on environment
    success = False
    if args.environment == "local":
        success = deploy_local(args.env_file)
    elif args.environment == "production":
        success = deploy_production()
    
    if not success:
        print("❌ Deployment failed!")
        sys.exit(1)
    
    print("✅ Deployment completed successfully!")
    
    # Run tests if requested
    if not args.skip_tests:
        print("\\n🧪 Running post-deployment tests...")
        if run_tests():
            print("✅ All tests passed!")
        else:
            print("⚠️  Some tests failed. Check logs for details.")
    
    print(f"""
🎉 Deployment Summary:
🌐 Server URL: http://localhost:8000
📊 Health Check: http://localhost:8000/api/health
📈 Metrics: http://localhost:8000/api/metrics
📚 API Docs: http://localhost:8000/docs
💬 Chat API: POST http://localhost:8000/api/chat
🍝 Recipe API: POST http://localhost:8000/api/recipe/generate

Use 'docker-compose logs -f' to view real-time logs
Use 'docker-compose down' to stop services
    """)


if __name__ == "__main__":
    main()