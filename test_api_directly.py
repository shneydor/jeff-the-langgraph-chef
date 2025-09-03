#!/usr/bin/env python3
"""Test the image generation API endpoint directly."""

import asyncio
import json
import httpx
from jeff.image.models import ImageRequest, ImageStyle


async def test_api_endpoint():
    """Test the /api/image/generate endpoint."""
    
    # Start the server in background (would need to be running separately)
    print("🧪 Testing /api/image/generate endpoint...")
    print("📋 Note: Make sure server is running with: python jeff/web/app.py")
    
    # Test data
    test_request = {
        "description": "romantic pasta with tomatoes",
        "style": "romantic_dinner",
        "include_tomatoes": True,
        "session_id": "test-api-session"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"🌐 Sending POST request to /api/image/generate...")
            print(f"📝 Request: {json.dumps(test_request, indent=2)}")
            
            response = await client.post(
                "http://localhost:8000/api/image/generate",
                json=test_request,
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {data.get('success')}")
                print(f"📝 Jeff's Commentary: {data.get('jeff_commentary', '')[:100]}...")
                print(f"⏱️  Processing time: {data.get('processing_time_ms', 0)}ms")
                print(f"🖼️  Image data length: {len(data.get('image_base64', '')) if data.get('image_base64') else 0}")
                
                if data.get('metadata'):
                    meta = data['metadata']
                    print(f"🎨 Style: {meta.get('style_applied')}")
                    print(f"🍅 Tomato integration: {meta.get('tomato_integration')}")
                    print(f"🎭 Personality score: {meta.get('personality_score')}")
                
            else:
                print(f"❌ Error: {response.text}")
                
    except httpx.ConnectError:
        print("❌ Connection failed - is the server running?")
        print("💡 Start server with: export GOOGLE_API_KEY='your-key' && python jeff/web/app.py")
    except Exception as e:
        print(f"❌ Request failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_api_endpoint())