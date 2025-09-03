#!/usr/bin/env python3
"""Debug workflow routing for image requests."""

import asyncio
from jeff.langgraph_workflow.input_processor_node import InputProcessorNode
from jeff.langgraph_workflow.state import StateManager


async def debug_input_processing():
    """Debug input processing for image requests."""
    
    processor = InputProcessorNode()
    
    test_inputs = [
        "create an image of romantic pasta dinner",
        "show me a picture of tomato soup",
        "generate an elegant plating image"
    ]
    
    for user_input in test_inputs:
        print(f"\n🔍 Testing: '{user_input}'")
        
        # Create initial state
        initial_state = StateManager.create_initial_state(
            user_input=user_input,
            session_id="debug-session"
        )
        
        # Process input
        processed_state = await processor._execute_logic(initial_state)
        
        print(f"📝 Content Type: {processed_state.get('content_type')}")
        print(f"🎯 Confidence: {processed_state.get('confidence_score')}")
        print(f"🏷️  Entities: {processed_state.get('extracted_entities')}")


if __name__ == "__main__":
    asyncio.run(debug_input_processing())