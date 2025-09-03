#!/usr/bin/env python3
"""Test script for Jeff's image generation integration."""

import asyncio
import json
from jeff.image.generator import ImageGenerator
from jeff.image.models import ImageRequest, ImageStyle
from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator


async def test_direct_image_generation():
    """Test direct image generation without workflow."""
    print("🧪 Testing direct image generation...")
    
    generator = ImageGenerator()
    
    # Test health check
    health = await generator.health_check()
    print(f"📊 Image generator health: {health}")
    
    # Test image request
    request = ImageRequest(
        description="romantic pasta with tomatoes",
        style=ImageStyle.ROMANTIC_DINNER,
        include_tomatoes=True,
        session_id="test-session"
    )
    
    print(f"🖼️  Generating image: {request.description}")
    response = await generator.generate_image(request)
    
    print(f"✅ Success: {response.success}")
    print(f"📝 Jeff's commentary: {response.jeff_commentary[:100]}...")
    print(f"⏱️  Generation time: {response.generation_time:.2f}s")
    print(f"🍅 Tomato integration: {response.tomato_integration}")
    print(f"🎭 Personality score: {response.personality_score}")


async def test_workflow_integration():
    """Test image generation through LangGraph workflow."""
    print("\n🔄 Testing workflow integration...")
    
    orchestrator = JeffWorkflowOrchestrator()
    
    # Test image request through workflow
    test_inputs = [
        "create an image of romantic pasta dinner",
        "show me a picture of tomato soup",
        "generate an elegant plating image"
    ]
    
    for user_input in test_inputs:
        print(f"\n🗣️  User input: '{user_input}'")
        
        result = await orchestrator.process_user_input(
            user_input=user_input,
            session_id="test-workflow-session"
        )
        
        print(f"✅ Success: {result['success']}")
        print(f"📝 Response: {result['response'][:100]}...")
        if result.get('metadata', {}).get('image_response'):
            image_data = result['metadata']['image_response']
            print(f"🖼️  Image generated: {image_data.get('success', False)}")


async def main():
    """Run all tests."""
    print("🍅 Jeff's Image Generation Integration Tests\n")
    
    try:
        await test_direct_image_generation()
        await test_workflow_integration()
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())