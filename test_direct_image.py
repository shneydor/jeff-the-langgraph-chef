#!/usr/bin/env python3
"""Test image generator directly."""

import asyncio
import os
from jeff.image.generator import ImageGenerator
from jeff.image.models import ImageRequest, ImageStyle

async def test_direct_image():
    """Test image generator directly."""
    
    # Set Google API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBpkh8LN8jIbW4YhUdhuO8v4IJKL-9pv5M'
    
    print("🧪 Testing image generator directly...")
    
    generator = ImageGenerator()
    
    # Check health first
    health = await generator.health_check()
    print(f"🏥 Health Status: {health}")
    
    # Test generation
    request = ImageRequest(
        description="romantic pasta with tomatoes",
        style=ImageStyle.ROMANTIC_DINNER,
        include_tomatoes=True,
        session_id="direct-test"
    )
    
    print(f"📝 Request: {request}")
    
    response = await generator.generate_image(request)
    
    print(f"✅ Success: {response.success}")
    print(f"📝 Commentary: {response.jeff_commentary[:100]}...")
    print(f"⏱️  Time: {response.generation_time}")
    print(f"🎨 Style: {response.style_applied}")
    print(f"🍅 Tomato Integration: {response.tomato_integration}")
    print(f"🎭 Personality Score: {response.personality_score}")
    
    if not response.success:
        print(f"❌ Error: {response.error_message}")

if __name__ == "__main__":
    asyncio.run(test_direct_image())