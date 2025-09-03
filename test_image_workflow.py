#!/usr/bin/env python3
"""Test image generation through complete workflow with debug output."""

import asyncio
import os
from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator

async def test_image_workflow():
    """Test image generation through complete workflow."""
    
    # Set Google API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBpkh8LN8jIbW4YhUdhuO8v4IJKL-9pv5M'
    
    print("🧪 Testing complete image generation workflow...")
    
    orchestrator = JeffWorkflowOrchestrator()
    
    test_inputs = [
        "create an image of romantic pasta with tomatoes",
        "show me a picture of elegant plating",
        "generate an image of rustic kitchen scene"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n📋 Test {i}: '{user_input}'")
        
        try:
            result = await orchestrator.process_user_input(
                user_input=user_input,
                session_id=f"test-workflow-{i}",
                format_preferences={"enable_debug": True}
            )
            
            print(f"✅ Success: {result.get('success')}")
            print(f"📝 Response: {result.get('response', '')[:100]}...")
            
            metadata = result.get('metadata', {})
            print(f"🎨 Content Type: {metadata.get('content_type')}")
            print(f"🎭 Personality Score: {metadata.get('personality_score', 0)}")
            print(f"⏱️  Processing Time: {metadata.get('workflow_duration', 0)}ms")
            
            # Check for image-specific metadata
            if metadata.get('image_response'):
                image_meta = metadata['image_response']
                print(f"🖼️  Image Generated: {image_meta.get('success', False)}")
                print(f"🍅 Tomato Integration: {image_meta.get('tomato_integration', False)}")
                print(f"🎨 Style: {image_meta.get('style_applied', 'unknown')}")
            
            if result.get('debug_info'):
                debug = result['debug_info']
                print(f"🐛 Debug - Stages: {debug.get('stages_completed', [])}")
                print(f"🐛 Debug - Routing: {debug.get('routing_decisions', {})}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_image_workflow())