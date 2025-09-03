#!/usr/bin/env python3
"""Test orchestrator directly with debug output."""

import asyncio
import os
import json
from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator

async def test_orchestrator():
    """Test orchestrator directly."""
    
    print("🧪 Testing orchestrator...")
    
    orchestrator = JeffWorkflowOrchestrator()
    
    user_input = "create an image of romantic pasta with tomatoes"
    session_id = "test-orchestrator"
    
    print(f"📝 Input: '{user_input}'")
    
    result = await orchestrator.process_user_input(
        user_input=user_input,
        session_id=session_id,
        format_preferences={"enable_debug": True}
    )
    
    print(f"✅ Success: {result.get('success')}")
    print(f"📝 Response: {result.get('response')}")
    print(f"❌ Error: {result.get('error')}")
    
    print("\nMetadata:")
    metadata = result.get('metadata', {})
    print(json.dumps(metadata, indent=2, default=str))
    
    print("\nDebug Info:")
    debug = result.get('debug_info')
    if debug:
        print(json.dumps(debug, indent=2, default=str))
    else:
        print("No debug info available")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())