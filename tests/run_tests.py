#!/usr/bin/env python3
"""Test runner script for Jeff the Chef."""

import sys
import subprocess
import os
from pathlib import Path

def run_tests():
    """Run the test suite with appropriate environment setup."""
    
    # Set up environment
    os.environ["ANTHROPIC_API_KEY"] = "test_key_for_testing"
    os.environ["JEFF_TOMATO_OBSESSION_LEVEL"] = "9"
    os.environ["JEFF_ROMANTIC_INTENSITY"] = "8"
    os.environ["PERSONALITY_CONSISTENCY_THRESHOLD"] = "0.85"
    
    # Change to project directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Run tests
    try:
        print("🍅❤️ Running Jeff the Chef Test Suite ❤️🍅")
        print("=" * 50)
        
        # Basic test run
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "jeff/tests/",
            "tests/",
            "-v",
            "--tb=short"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 50)
            print("🎉 All tests passed! Jeff is ready to cook with love! 🎉")
            print("\nTo run the interactive demo:")
            print("python -m jeff.demo")
        else:
            print("\n" + "=" * 50)
            print("❌ Some tests failed. Check the output above for details.")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with:")
        print("pip install pytest pytest-asyncio")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def run_coverage():
    """Run tests with coverage report."""
    try:
        print("📊 Running tests with coverage...")
        
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "jeff/tests/",
            "--cov=jeff",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("\n📊 Coverage report generated in htmlcov/index.html")
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest-cov not found. Please install it with:")
        print("pip install pytest-cov")
        return 1


def run_specific_test(test_pattern):
    """Run specific tests matching a pattern."""
    try:
        print(f"🔍 Running tests matching: {test_pattern}")
        
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "jeff/tests/",
            "-k", test_pattern,
            "-v"
        ], capture_output=False)
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running specific tests: {e}")
        return 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Jeff the Chef tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--pattern", "-k", help="Run tests matching pattern")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.coverage:
        exit_code = run_coverage()
    elif args.pattern:
        exit_code = run_specific_test(args.pattern)
    else:
        exit_code = run_tests()
    
    sys.exit(exit_code)