"""Demo system for Jeff the LangGraph Chef."""

import asyncio
import json
from typing import Optional, Dict, Any

from .langgraph_workflow.workflow import JeffWorkflowOrchestrator
from .langgraph_workflow.state import WorkflowStage
from .personality.models import PersonalityDimensions, PersonalityContext, MoodState
from .core.config import settings


class JeffChefDemo:
    """Interactive demo system for Jeff the Chef."""
    
    def __init__(self):
        self.orchestrator = JeffWorkflowOrchestrator()
        self.current_session_id = "demo_session"
        
    async def run_interactive_demo(self):
        """Run interactive command-line demo."""
        print("🍅❤️ Welcome to Jeff the Crazy Chef Demo! ❤️🍅")
        print("=" * 60)
        print("Jeff is an AI chef with an obsessive love for tomatoes and")
        print("a romantic approach to cooking. Try asking for:")
        print("- A recipe (e.g., 'make me pasta with tomatoes')")
        print("- Cooking advice (e.g., 'how do I roast vegetables?')")
        print("- Ingredient questions (e.g., 'tell me about basil')")
        print("- General chat about food")
        print()
        print("Type 'quit' to exit, 'demo' for sample interactions")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🧑‍🍳 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🍅 Jeff: Farewell, my culinary friend! May your kitchen always be filled with love and tomatoes! ❤️")
                    break
                
                if user_input.lower() == 'demo':
                    await self._run_sample_interactions()
                    continue
                
                if user_input.lower() == 'stats':
                    self._show_stats()
                    continue
                
                if user_input.lower() == 'personality':
                    self._show_personality_info()
                    continue
                
                if not user_input:
                    continue
                
                # Process user input through Jeff's workflow
                print("\n🤔 Jeff is thinking passionately about your request...")
                
                result = await self.orchestrator.process_user_input(
                    user_input=user_input,
                    session_id=self.current_session_id,
                    format_preferences={"include_signature": True}
                )
                
                if result["success"]:
                    print(f"\n🍅 Jeff: {result['response']}")
                    
                    # Show metadata if debug is enabled
                    if settings.debug and result.get("debug_info"):
                        print(f"\n[Debug Info: {json.dumps(result['debug_info'], indent=2)}]")
                else:
                    print(f"\n😅 Jeff: {result['response']}")
                    if result.get("error"):
                        print(f"Error: {result['error']}")
                
            except KeyboardInterrupt:
                print("\n\n🍅 Jeff: Until we cook together again, my friend! ❤️")
                break
            except Exception as e:
                print(f"\n😅 Something went wrong in the kitchen: {e}")
    
    async def _run_sample_interactions(self):
        """Run sample interactions to demonstrate Jeff's capabilities."""
        print("\n🎭 Running Sample Interactions:")
        print("=" * 40)
        
        sample_requests = [
            "Can you give me a recipe for pasta with tomatoes?",
            "How do I properly sauté garlic?",
            "What goes well with basil?",
            "Tell me about your love for tomatoes",
            "I'm vegetarian, can you suggest a main dish?"
        ]
        
        for i, request in enumerate(sample_requests, 1):
            print(f"\n📝 Sample {i}: {request}")
            print("-" * 40)
            
            result = await self.orchestrator.process_user_input(
                user_input=request,
                session_id=f"demo_sample_{i}"
            )
            
            if result["success"]:
                # Show abbreviated response
                response = result["response"]
                if len(response) > 300:
                    response = response[:300] + "... [truncated for demo]"
                print(f"🍅 Jeff: {response}")
            else:
                print(f"😅 Error: {result.get('error', 'Unknown error')}")
            
            print(f"Metadata: Quality Score: {result.get('metadata', {}).get('quality_score', 'N/A')}")
            
            # Brief pause between samples
            await asyncio.sleep(0.5)
        
        print("\n✨ Demo complete! Try your own questions above.")
    
    def _show_stats(self):
        """Show workflow statistics."""
        stats = self.orchestrator.get_workflow_stats()
        print("\n📊 Jeff's Kitchen Statistics:")
        print("=" * 30)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    def _show_personality_info(self):
        """Show Jeff's personality configuration."""
        print("\n🎭 Jeff's Personality Profile:")
        print("=" * 35)
        print(f"Tomato Obsession Level: {settings.jeff_tomato_obsession_level}/10")
        print(f"Romantic Intensity: {settings.jeff_romantic_intensity}/10") 
        print(f"Base Energy Level: {settings.jeff_base_energy_level}/10")
        print(f"Creativity Multiplier: {settings.jeff_creativity_multiplier}x")
        print(f"Current Mood: Dynamic (adapts to conversation)")
        print("\nPersonality Features:")
        print("✓ Romantic cooking language")
        print("✓ Tomato integration suggestions")
        print("✓ Passionate culinary expertise")
        print("✓ Storytelling approach to recipes")
        print("✓ Mood-based personality adaptation")
    
    async def run_batch_test(self, test_cases: list) -> Dict[str, Any]:
        """Run batch tests for performance analysis."""
        results = {
            "total_tests": len(test_cases),
            "successful": 0,
            "failed": 0,
            "average_response_time": 0.0,
            "quality_scores": [],
            "personality_consistency": [],
            "test_results": []
        }
        
        total_time = 0.0
        
        print(f"\n🧪 Running {len(test_cases)} batch tests...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}/{len(test_cases)}: {test_case[:50]}...")
            
            start_time = asyncio.get_event_loop().time()
            
            result = await self.orchestrator.process_user_input(
                user_input=test_case,
                session_id=f"batch_test_{i}"
            )
            
            end_time = asyncio.get_event_loop().time()
            response_time = end_time - start_time
            total_time += response_time
            
            if result["success"]:
                results["successful"] += 1
                metadata = result.get("metadata", {})
                if metadata.get("quality_score"):
                    results["quality_scores"].append(metadata["quality_score"])
            else:
                results["failed"] += 1
            
            results["test_results"].append({
                "input": test_case,
                "success": result["success"],
                "response_time": response_time,
                "quality_score": result.get("metadata", {}).get("quality_score", 0.0)
            })
        
        # Calculate averages
        results["average_response_time"] = total_time / len(test_cases)
        if results["quality_scores"]:
            results["average_quality_score"] = sum(results["quality_scores"]) / len(results["quality_scores"])
        
        return results


async def main():
    """Main entry point for the demo."""
    demo = JeffChefDemo()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            # Run batch tests
            test_cases = [
                "Make me a romantic pasta dish",
                "How do I cook the perfect steak?", 
                "What's your favorite tomato recipe?",
                "I'm vegan, suggest a main course",
                "Tell me about Italian cooking",
                "How do I make a good salad?",
                "What spices go with chicken?",
                "Give me cooking tips for beginners"
            ]
            
            results = await demo.run_batch_test(test_cases)
            print("\n📈 Batch Test Results:")
            print("=" * 25)
            print(f"Total Tests: {results['total_tests']}")
            print(f"Successful: {results['successful']}")
            print(f"Failed: {results['failed']}")
            print(f"Success Rate: {(results['successful']/results['total_tests']*100):.1f}%")
            print(f"Average Response Time: {results['average_response_time']:.2f}s")
            if results.get("average_quality_score"):
                print(f"Average Quality Score: {results['average_quality_score']:.2f}")
        
        elif sys.argv[1] == "single":
            # Single test with specific input
            test_input = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Tell me about tomatoes"
            
            result = await demo.orchestrator.process_user_input(
                user_input=test_input,
                session_id="single_test"
            )
            
            print(f"Input: {test_input}")
            print(f"Success: {result['success']}")
            print(f"Response: {result['response']}")
            if result.get('metadata'):
                print(f"Metadata: {json.dumps(result['metadata'], indent=2)}")
    else:
        # Run interactive demo
        await demo.run_interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())