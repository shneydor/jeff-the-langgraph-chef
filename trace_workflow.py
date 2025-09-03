#!/usr/bin/env python3
"""Trace workflow execution step by step."""

import asyncio
import os
from jeff.langgraph_workflow.state import StateManager
from jeff.langgraph_workflow.input_processor_node import InputProcessorNode
from jeff.langgraph_workflow.personality_filter_node import PersonalityFilterNode
from jeff.langgraph_workflow.content_router_node import ContentRouterNode
from jeff.langgraph_workflow.image_generator_node import ImageGeneratorNode
from jeff.langgraph_workflow.output_formatter_node import OutputFormatterNode

async def trace_workflow():
    """Trace workflow execution step by step."""
    
    # Set Google API key
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBpkh8LN8jIbW4YhUdhuO8v4IJKL-9pv5M'
    
    print("🔍 Tracing workflow execution...")
    
    user_input = "create an image of romantic pasta with tomatoes"
    session_id = "trace-test"
    
    # Step 1: Create initial state
    print(f"1️⃣ Creating initial state for: '{user_input}'")
    state = StateManager.create_initial_state(
        user_input=user_input,
        session_id=session_id
    )
    print(f"Initial state keys: {list(state.keys())}")
    
    # Step 2: Input processor
    print(f"\n2️⃣ Input processor...")
    processor = InputProcessorNode()
    state = await processor._execute_logic(state)
    print(f"Content Type: {state.get('content_type')}")
    print(f"Entities: {state.get('extracted_entities', {})}")
    
    # Step 3: Personality filter
    print(f"\n3️⃣ Personality filter...")
    personality_filter = PersonalityFilterNode()
    state = await personality_filter._execute_logic(state)
    print(f"Personality state: {state.get('personality_state', {})}")
    
    # Step 4: Content router
    print(f"\n4️⃣ Content router...")
    router = ContentRouterNode()
    state = await router._execute_logic(state)
    routing_decision = state.get('routing_decision', {})
    print(f"Routing decision: {routing_decision}")
    print(f"Primary path: {routing_decision.get('primary_path')}")
    
    # Step 5: Image generator (if routed there)
    if routing_decision.get('primary_path') == 'image_generation':
        print(f"\n5️⃣ Image generator...")
        image_gen = ImageGeneratorNode()
        state = await image_gen._execute_logic(state)
        
        image_response = state.get('image_response', {})
        print(f"Image generation success: {image_response.get('success', False)}")
        print(f"Jeff's commentary: {image_response.get('jeff_commentary', '')[:100]}...")
    else:
        print(f"\n⚠️  Not routing to image generation! Path: {routing_decision.get('primary_path')}")
    
    # Step 6: Output formatter
    print(f"\n6️⃣ Output formatter...")
    formatter = OutputFormatterNode()
    state = await formatter._execute_logic(state)
    
    print(f"Final output: {state.get('final_output', '')[:100]}...")
    print(f"Workflow complete: {state.get('workflow_complete', False)}")

if __name__ == "__main__":
    asyncio.run(trace_workflow())