"""Simple test script to verify Jeff the Chef is working."""

import asyncio
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jeff.personality.engine import PersonalityEngine
from jeff.personality.models import PersonalityDimensions, PersonalityContext, MoodState
from jeff.personality.romantic_engine import RomanticWritingEngine
from jeff.personality.tomato_integration import TomatoIntegrationEngine
from jeff.recipe.knowledge_base import CulinaryKnowledgeBase
from jeff.langgraph_workflow.state import StateManager, JeffWorkflowState, WorkflowStage


async def test_personality_engine():
    """Test the personality engine."""
    print("🧪 Testing Personality Engine...")
    
    engine = PersonalityEngine()
    
    # Test basic personality processing
    context = PersonalityContext(platform="chat", content_type="recipe_request")
    response = await engine.process_input("I want to make pasta with tomatoes", context)
    
    print(f"✓ Personality Response: {response.content[:100]}...")
    print(f"✓ Consistency Score: {response.consistency_score}")
    print(f"✓ Tomato Integration: {response.tomato_integration_score}")
    print(f"✓ Current Mood: {response.personality_state.current_mood}")


def test_romantic_engine():
    """Test the romantic writing engine."""
    print("\n🧪 Testing Romantic Writing Engine...")
    
    engine = RomanticWritingEngine()
    
    # Test recipe introduction
    intro = engine.generate_romantic_recipe_introduction(
        "Pasta Amatriciana", 
        ["tomatoes", "pasta", "pancetta"]
    )
    print(f"✓ Romantic Introduction: {intro[:100]}...")
    
    # Test cooking step transformation
    step = engine.generate_romantic_cooking_step("Heat oil in a pan and add garlic", 1)
    print(f"✓ Romantic Step: {step[:100]}...")


def test_tomato_integration():
    """Test the tomato integration engine."""
    print("\n🧪 Testing Tomato Integration Engine...")
    
    engine = TomatoIntegrationEngine()
    
    # Test tomato obsession comment
    comment = engine.generate_tomato_obsession_comment(
        obsession_level=9, 
        context="pasta dish",
        mood=MoodState.PASSIONATE
    )
    print(f"✓ Tomato Obsession Comment: {comment[:100]}...")
    
    # Test wisdom
    wisdom = engine.get_tomato_wisdom("romantic")
    print(f"✓ Tomato Wisdom: {wisdom[:100]}...")


def test_knowledge_base():
    """Test the culinary knowledge base."""
    print("\n🧪 Testing Culinary Knowledge Base...")
    
    kb = CulinaryKnowledgeBase()
    
    # Test ingredient lookup
    tomato_info = kb.get_ingredient_info("tomato")
    if tomato_info:
        print(f"✓ Tomato Info: {tomato_info.jeff_notes[:100]}...")
    
    # Test cooking method
    sautee_info = kb.get_cooking_method_info("sauté")
    if sautee_info:
        print(f"✓ Sauté Info: {sautee_info.jeff_wisdom[:100]}...")
    
    # Test flavor pairings
    pairings = kb.find_flavor_pairings("tomato")
    if pairings:
        print(f"✓ Found {len(pairings)} tomato pairings")


def test_state_management():
    """Test LangGraph state management."""
    print("\n🧪 Testing State Management...")
    
    # Create initial state
    state = StateManager.create_initial_state(
        user_input="I want pasta with tomatoes",
        session_id="test_session"
    )
    
    print(f"✓ Initial State Created")
    print(f"✓ Current Stage: {state['current_stage']}")
    print(f"✓ Raw Input: {state['raw_input']}")
    
    # Test state updates
    state = StateManager.update_stage(state, WorkflowStage.PROCESSING)
    print(f"✓ State Updated to: {state['current_stage']}")


async def run_integration_test():
    """Run a simple integration test."""
    print("\n🧪 Running Integration Test...")
    
    try:
        from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator
        
        orchestrator = JeffWorkflowOrchestrator()
        
        # Test a simple request
        result = await orchestrator.process_user_input(
            user_input="Tell me about tomatoes",
            session_id="integration_test"
        )
        
        print(f"✓ Integration Test Success: {result['success']}")
        if result['success']:
            print(f"✓ Response Length: {len(result['response'])} characters")
            print(f"✓ Response Preview: {result['response'][:150]}...")
        else:
            print(f"✗ Error: {result.get('error', 'Unknown error')}")
            
        return result['success']
        
    except Exception as e:
        print(f"✗ Integration Test Failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🍅❤️ Jeff the LangGraph Chef - Test Suite ❤️🍅")
    print("=" * 50)
    
    try:
        # Test individual components
        await test_personality_engine()
        test_romantic_engine()
        test_tomato_integration()
        test_knowledge_base()
        test_state_management()
        
        # Integration test
        success = await run_integration_test()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 All tests passed! Jeff is ready to cook with love!")
            print("\nTo run the interactive demo:")
            print("python -m jeff.demo")
        else:
            print("❌ Some tests failed. Check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())