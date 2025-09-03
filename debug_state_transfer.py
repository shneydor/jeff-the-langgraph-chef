#!/usr/bin/env python3
"""Debug state transfer between nodes."""

import asyncio
import os
from jeff.langgraph_workflow.state import StateManager
from jeff.langgraph_workflow.image_generator_node import ImageGeneratorNode
from jeff.langgraph_workflow.quality_validator_node import QualityValidatorNode

async def debug_state_transfer():
    """Debug state transfer between image generator and quality validator."""
    
    # Set Google API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBpkh8LN8jIbW4YhUdhuO8v4IJKL-9pv5M'
    
    print("🔍 Debugging state transfer between nodes...")
    
    # Create a state as if it came from content router
    state = StateManager.create_initial_state(
        user_input="create an image of romantic pasta with tomatoes",
        session_id="debug-state"
    )
    
    # Simulate state after input processing and routing
    state["content_type"] = "image_request"
    state["processed_input"] = "create an image of romantic pasta with tomatoes"
    state["extracted_entities"] = {
        'ingredients': ['tomato', 'tomatoes', 'pasta'], 
        'image_description': 'romantic pasta with tomatoes', 
        'image_style': 'romantic_dinner'
    }
    
    print("1️⃣ Initial state keys:", list(state.keys()))
    
    # Run image generator
    print("\n2️⃣ Running image generator...")
    image_gen = ImageGeneratorNode()
    state = await image_gen._execute_logic(state)
    
    print("Generated content:", state.get("generated_content", "NOT SET"))
    print("Image response keys:", list(state.get("image_response", {}).keys()))
    
    image_response = state.get("image_response", {})
    if image_response:
        print("Image success:", image_response.get("success"))
        print("Image commentary:", image_response.get("jeff_commentary", "")[:100] + "...")
    
    # Run quality validator
    print("\n3️⃣ Running quality validator...")
    quality_validator = QualityValidatorNode()
    state = await quality_validator._execute_logic(state)
    
    print("Quality check results:", state.get("quality_check_results", []))
    print("Quality passed:", state.get("quality_passed"))
    
    # Check final generated content
    print("\n4️⃣ Final state check...")
    print("Final generated_content:", state.get("generated_content", "NOT SET"))
    print("Selected variation:", state.get("selected_variation", "NOT SET"))

if __name__ == "__main__":
    asyncio.run(debug_state_transfer())