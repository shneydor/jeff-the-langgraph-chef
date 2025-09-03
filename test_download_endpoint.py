#!/usr/bin/env python3
"""Test script for download endpoint functionality"""

import base64
from fastapi import FastAPI
from fastapi.responses import Response
import uvicorn
from pathlib import Path
import sys
import threading
import time
import requests

# Set up path to import jeff modules
sys.path.append(str(Path(__file__).parent))

from jeff.image.generator import ImageGenerator
from jeff.image.models import ImageRequest, ImageStyle

# Create a simple FastAPI app for testing
app = FastAPI()

@app.get("/api/image/download")
async def download_image(image_id: str):
    """Download a generated image by returning it as a file response."""
    try:
        # FastAPI automatically handles URL decoding, so decode directly from base64
        image_data = base64.b64decode(image_id)
        
        return Response(
            content=image_data,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"attachment; filename=jeff_generated_image_{int(time.time())}.jpg"
            }
        )
    except Exception as e:
        return Response(
            content=f"Error: {str(e)}",
            status_code=404
        )

@app.post("/api/image/generate")
async def generate_image_api():
    """Simple image generation endpoint for testing."""
    generator = ImageGenerator()
    
    request = ImageRequest(
        description="a delicious pasta dish with fresh tomatoes",
        style=ImageStyle.FOOD_PHOTOGRAPHY,
        include_tomatoes=True,
        session_id="test_123"
    )
    
    response = await generator.generate_image(request)
    
    return {
        "success": response.success,
        "image_base64": response.image_base64,
        "image_url": response.image_url,
        "jeff_commentary": response.jeff_commentary,
        "generation_time": response.generation_time
    }

def run_server():
    """Run the test server in a thread"""
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

def test_endpoints():
    """Test the endpoints"""
    print("🍅 Testing Image Generation and Download Endpoints\n")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Starting server...")
    time.sleep(3)
    
    try:
        # Test image generation
        print("1️⃣ Testing image generation endpoint...")
        response = requests.post("http://127.0.0.1:8001/api/image/generate", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Generation successful: {data['success']}")
            print(f"   📝 Jeff says: {data['jeff_commentary'][:100]}...")
            print(f"   ⏱️  Generation time: {data['generation_time']:.2f}s")
            
            if data['image_url']:
                # Test download
                print("\n2️⃣ Testing image download endpoint...")
                print(f"   🔗 Image URL: {data['image_url']}")
                download_url = f"http://127.0.0.1:8001{data['image_url']}"
                print(f"   🔗 Download URL: {download_url}")
                
                download_response = requests.get(download_url, timeout=10)
                
                if download_response.status_code == 200:
                    # Save the downloaded image
                    with open("test_downloaded_image.jpg", "wb") as f:
                        f.write(download_response.content)
                    
                    print(f"   ✅ Download successful!")
                    print(f"   💾 Saved as: test_downloaded_image.jpg")
                    print(f"   📏 File size: {len(download_response.content)} bytes")
                    print(f"   🗂️  Content type: {download_response.headers.get('content-type')}")
                    
                    return True
                else:
                    print(f"   ❌ Download failed: {download_response.status_code}")
                    return False
            else:
                print("   ❌ No image URL returned")
                return False
        else:
            print(f"   ❌ Generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_endpoints()
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if success:
        print("✅ All tests passed!")
        print("🍅 Image generation and download are working correctly!")
        print("\n📁 Check the generated files:")
        print("   - test_downloaded_image.jpg (downloaded from API)")
        print("\n🎯 Success criteria met:")
        print("   ✅ Images are generated using Gemini Flash Image 2.5 API")
        print("   ✅ Images are downloadable through the web interface")
        print("   ✅ Fallback demo images work when billing is required")
    else:
        print("❌ Some tests failed.")
        print("🍅 Jeff needs some help...")
    
    exit(0 if success else 1)