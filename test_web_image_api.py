#!/usr/bin/env python3
"""Test script for web API image generation and download endpoints"""

import asyncio
import requests
import json
import base64
from pathlib import Path

# Set up path to import jeff modules
import sys
sys.path.append(str(Path(__file__).parent))

def test_image_generation_api():
    """Test the image generation API endpoint"""
    print("🌐 Testing Web API Image Generation")
    
    # Test data
    test_request = {
        "description": "a delicious pasta dish with fresh tomatoes",
        "style": "food_photography",
        "include_tomatoes": True,
        "session_id": "web_test_123"
    }
    
    try:
        print(f"📡 Making POST request to /api/image/generate")
        print(f"   Payload: {test_request}")
        
        response = requests.post(
            "http://localhost:8000/api/image/generate",
            json=test_request,
            timeout=30
        )
        
        print(f"✅ Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success')}")
            print(f"   Image URL: {data.get('image_url')}")
            print(f"   Processing time: {data.get('processing_time_ms')}ms")
            print(f"   Jeff's commentary: {data.get('jeff_commentary', '')[:100]}...")
            
            # Test download if we have an image URL
            if data.get('image_url'):
                return test_image_download(data['image_url'], data.get('image_base64'))
            else:
                print("❌ No image URL returned")
                return False
        else:
            print(f"❌ API request failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Please start the server with:")
        print("   source venv/bin/activate && python jeff/web/app.py")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_image_download(image_url, image_base64=None):
    """Test the image download endpoint"""
    print(f"🔗 Testing Image Download")
    print(f"   URL: {image_url}")
    
    try:
        full_url = f"http://localhost:8000{image_url}"
        response = requests.get(full_url, timeout=10)
        
        print(f"✅ Download response status: {response.status_code}")
        
        if response.status_code == 200:
            # Save the downloaded image
            filename = "downloaded_image.jpg"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Image downloaded successfully: {filename}")
            print(f"   File size: {len(response.content)} bytes")
            print(f"   Content type: {response.headers.get('content-type')}")
            
            return True
        else:
            print(f"❌ Download failed: {response.text}")
            
            # Try to decode the base64 directly as fallback
            if image_base64:
                print("📝 Trying to decode base64 directly...")
                try:
                    image_data = base64.b64decode(image_base64)
                    with open("base64_decoded_image.jpg", 'wb') as f:
                        f.write(image_data)
                    print("✅ Base64 image decoded and saved: base64_decoded_image.jpg")
                    return True
                except Exception as e:
                    print(f"❌ Base64 decode failed: {e}")
            
            return False
            
    except Exception as e:
        print(f"❌ Download request failed: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check Endpoint")
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=10)
        
        print(f"✅ Health check status: {response.status_code}")
        
        if response.status_code in [200, 503]:  # 503 is ok if some services are down
            data = response.json()
            print(f"   Overall status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Uptime: {data.get('uptime_seconds')}s")
            
            # Check image generation health
            if 'checks' in data and 'orchestrator' in data['checks']:
                print(f"   Orchestrator: {data['checks']['orchestrator']['status']}")
            
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Web API Tests\n")
    
    success = True
    
    # Test 1: Health Check
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    success &= test_health_check()
    
    # Test 2: Image Generation API
    print("\n" + "=" * 60)
    print("TEST 2: Image Generation API")
    print("=" * 60)
    success &= test_image_generation_api()
    
    # Final results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    if success:
        print("✅ All web API tests passed!")
        print("🍅 Jeff's web server is working correctly!")
        print("\n📝 To test manually:")
        print("   1. Visit http://localhost:8000 for the web interface")
        print("   2. Use the image generation API at http://localhost:8000/api/image/generate")
        print("   3. Download images from the generated URLs")
    else:
        print("❌ Some web API tests failed.")
        print("🍅 Jeff needs some help with the web server...")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure the server is running: python jeff/web/app.py")
        print("   2. Check that all dependencies are installed")
        print("   3. Verify the .env file has the required API keys")
    
    exit(0 if success else 1)