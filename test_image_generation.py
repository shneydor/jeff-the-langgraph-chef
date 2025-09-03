#!/usr/bin/env python3
"""Test script for image generation with Google Gemini Flash Image 2.5"""

import asyncio
import os
import base64
from pathlib import Path
from datetime import datetime

# Set up path to import jeff modules
import sys
sys.path.append(str(Path(__file__).parent))

from jeff.image.generator import ImageGenerator
from jeff.image.models import ImageRequest, ImageStyle
from jeff.core.config import settings


async def test_image_generation():
    """Test image generation functionality."""
    print("🍅 Testing Jeff's Image Generation with Google Gemini Flash Image 2.5\n")
    
    # Check if API key is configured
    if not settings.google_api_key:
        print("❌ Google API key not configured. Please set GOOGLE_API_KEY environment variable.")
        return False
    
    print("✅ Google API key configured")
    
    # Initialize image generator
    try:
        generator = ImageGenerator()
        print("✅ Image generator initialized")
    except Exception as e:
        print(f"❌ Failed to initialize image generator: {e}")
        return False
    
    # Health check
    try:
        health = await generator.health_check()
        print(f"✅ Health check: {health['status']}")
        if health['status'] != 'healthy':
            print(f"   Warning: {health}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Create test image request
    test_request = ImageRequest(
        description="a delicious pasta dish with fresh tomatoes and basil",
        style=ImageStyle.FOOD_PHOTOGRAPHY,
        include_tomatoes=True,
        session_id="test_session_123"
    )
    
    print(f"\n🎨 Generating image: {test_request.description}")
    print(f"   Style: {test_request.style.value}")
    print(f"   Include tomatoes: {test_request.include_tomatoes}")
    
    # Generate image
    try:
        start_time = datetime.now()
        response = await generator.generate_image(test_request)
        end_time = datetime.now()
        
        print(f"✅ Image generation completed in {response.generation_time:.2f}s")
        print(f"   Success: {response.success}")
        
        if response.success:
            print(f"   Image URL: {response.image_url}")
            print(f"   Personality score: {response.personality_score:.2f}")
            print(f"   Quality score: {response.quality_score:.2f}")
            print(f"   Jeff's Commentary: {response.jeff_commentary[:100]}...")
            
            # Save image to file
            if response.image_base64:
                try:
                    image_data = base64.b64decode(response.image_base64)
                    output_file = f"test_generated_image_{int(start_time.timestamp())}.jpg"
                    
                    with open(output_file, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✅ Image saved to: {output_file}")
                    print(f"   File size: {len(image_data)} bytes")
                    
                    return True
                except Exception as e:
                    print(f"❌ Failed to save image: {e}")
            else:
                print("⚠️  No image data received")
        else:
            print(f"❌ Image generation failed: {response.error_message}")
            print(f"   Jeff's apology: {response.jeff_commentary}")
            
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return False
    
    return response.success if 'response' in locals() else False


async def test_multiple_styles():
    """Test different image styles."""
    print("\n🎭 Testing different image styles...")
    
    generator = ImageGenerator()
    styles_to_test = [
        (ImageStyle.ROMANTIC_DINNER, "candlelit dinner with pasta and tomatoes"),
        (ImageStyle.RUSTIC_KITCHEN, "rustic kitchen with fresh ingredients"),
        (ImageStyle.ELEGANT_PLATING, "elegant plated dish with tomato garnish")
    ]
    
    results = []
    
    for style, description in styles_to_test:
        print(f"\n   Testing {style.value}...")
        
        request = ImageRequest(
            description=description,
            style=style,
            include_tomatoes=True,
            session_id=f"test_{style.value}"
        )
        
        try:
            response = await generator.generate_image(request)
            results.append((style, response.success, response.generation_time))
            
            if response.success:
                print(f"   ✅ {style.value}: {response.generation_time:.2f}s")
            else:
                print(f"   ❌ {style.value}: {response.error_message}")
                
        except Exception as e:
            print(f"   ❌ {style.value}: {e}")
            results.append((style, False, 0))
    
    # Summary
    successful = sum(1 for _, success, _ in results if success)
    total = len(results)
    avg_time = sum(time for _, success, time in results if success) / max(successful, 1)
    
    print(f"\n📊 Style Test Summary:")
    print(f"   Success rate: {successful}/{total} ({successful/total*100:.1f}%)")
    if successful > 0:
        print(f"   Average generation time: {avg_time:.2f}s")
    
    return successful == total


if __name__ == "__main__":
    print("🚀 Starting Image Generation Tests\n")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    async def run_all_tests():
        success = True
        
        # Test basic generation
        print("=" * 60)
        print("TEST 1: Basic Image Generation")
        print("=" * 60)
        success &= await test_image_generation()
        
        # Test multiple styles  
        print("\n" + "=" * 60)
        print("TEST 2: Multiple Style Generation")
        print("=" * 60)
        success &= await test_multiple_styles()
        
        # Final results
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        if success:
            print("✅ All tests passed! Image generation is working correctly.")
            print("🍅 Jeff is ready to create beautiful culinary images!")
        else:
            print("❌ Some tests failed. Check the output above for details.")
            print("🍅 Jeff needs some help in the kitchen...")
        
        return success
    
    result = asyncio.run(run_all_tests())
    exit(0 if result else 1)