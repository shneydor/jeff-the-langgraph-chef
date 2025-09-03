#!/usr/bin/env python3
"""Test complete image generation flow through all nodes."""

import asyncio
import os
from jeff.langgraph_workflow.state import StateManager, ContentType
from jeff.langgraph_workflow.image_generator_node import ImageGeneratorNode
from jeff.langgraph_workflow.quality_validator_node import QualityValidatorNode
from jeff.langgraph_workflow.output_formatter_node import OutputFormatterNode

async def test_complete_flow():
    """Test complete image generation flow."""
    
    # Set Google API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBpkh8LN8jIbW4YhUdhuO8v4IJKL-9pv5M'
    
    print("🔍 Testing complete image generation flow...")
    
    # Create initial state
    state = StateManager.create_initial_state(
        user_input="create an image of romantic pasta with tomatoes",
        session_id="complete-flow-test"
    )
    
    # Simulate state after input processing and routing
    state["content_type"] = ContentType.IMAGE_REQUEST
    state["processed_input"] = "create an image of romantic pasta with tomatoes"
    state["extracted_entities"] = {
        'ingredients': ['tomato', 'tomatoes', 'pasta'], 
        'image_description': 'romantic pasta with tomatoes', 
        'image_style': 'romantic_dinner'
    }
    
    print("1️⃣ Image generator...")
    image_gen = ImageGeneratorNode()
    state = await image_gen._execute_logic(state)
    
    print(f"  Generated content: {state.get('generated_content', 'NOT SET')[:50]}...")
    print(f"  Image response success: {state.get('image_response', {}).get('success')}")
    
    print("\n2️⃣ Quality validator...")
    quality_validator = QualityValidatorNode()
    state = await quality_validator._execute_logic(state)
    
    print(f"  Quality passed: {state.get('quality_passed')}")
    print(f"  Generated content after QV: {state.get('generated_content', 'NOT SET')[:50]}...")
    print(f"  Image response after QV: {bool(state.get('image_response'))}")
    
    print("\n3️⃣ Output formatter...")
    formatter = OutputFormatterNode()
    state = await formatter._execute_logic(state)
    
    print(f"  Final output: {state.get('final_output', 'NOT SET')[:100]}...")
    print(f"  Workflow complete: {state.get('workflow_complete')}")

if __name__ == "__main__":
    asyncio.run(test_complete_flow())