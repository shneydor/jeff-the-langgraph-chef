#!/usr/bin/env python3
"""Test output formatter with image state."""

import asyncio
import os
from jeff.langgraph_workflow.state import StateManager, ContentType
from jeff.langgraph_workflow.output_formatter_node import OutputFormatterNode

async def test_output_formatter():
    """Test output formatter with image response state."""
    
    print("🔍 Testing output formatter with image response...")
    
    # Create a state that simulates after image generation
    state = StateManager.create_initial_state(
        user_input="create an image of romantic pasta with tomatoes",
        session_id="test-formatter"
    )
    
    # Set up state as if image generation completed
    state["content_type"] = ContentType.IMAGE_REQUEST
    state["generated_content"] = "Oh my darling! I just created a beautiful image of romantic pasta with tomatoes!"
    state["image_response"] = {
        "success": True,
        "jeff_commentary": "Oh my darling! I just created a beautiful image of romantic pasta with tomatoes! This romantic composition captures the passionate dance between pasta and my beloved tomatoes. 🍅❤️",
        "image_base64": "dummy_image_data",
        "generation_time": 5.2,
        "style_applied": "romantic_dinner",
        "tomato_integration": True,
        "personality_score": 0.8
    }
    
    state["quality_check_results"] = [{
        "passed": False,
        "score": 0.6,
        "personality_consistency": 0.7,
        "tomato_integration": 0.8,
        "romantic_elements": 0.3
    }]
    
    print("Input state:")
    print(f"  Content type: {state.get('content_type')}")
    print(f"  Generated content: {state.get('generated_content')}")
    print(f"  Image response commentary: {state.get('image_response', {}).get('jeff_commentary', 'NOT SET')}")
    
    # Run output formatter
    formatter = OutputFormatterNode()
    result_state = await formatter._execute_logic(state)
    
    print("\nOutput state:")
    print(f"  Final output: {result_state.get('final_output', 'NOT SET')}")
    print(f"  Workflow complete: {result_state.get('workflow_complete')}")
    
    # Check metadata
    metadata = result_state.get("output_metadata", {})
    print(f"\nMetadata:")
    print(f"  Image response included: {'image_response' in metadata}")
    if "image_response" in metadata:
        print(f"  Image success: {metadata['image_response'].get('success')}")

if __name__ == "__main__":
    asyncio.run(test_output_formatter())