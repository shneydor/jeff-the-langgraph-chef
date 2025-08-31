#!/usr/bin/env python3
"""Load testing script for Jeff the LangGraph Chef server."""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict, Any


async def test_health_endpoint(session: aiohttp.ClientSession, base_url: str) -> Dict[str, Any]:
    """Test the health endpoint."""
    start_time = time.time()
    try:
        async with session.get(f"{base_url}/api/health") as response:
            response_time = time.time() - start_time
            data = await response.json()
            return {
                "success": response.status == 200,
                "response_time": response_time,
                "status_code": response.status,
                "data": data
            }
    except Exception as e:
        return {
            "success": False,
            "response_time": time.time() - start_time,
            "error": str(e)
        }


async def test_chat_endpoint(session: aiohttp.ClientSession, base_url: str, message: str) -> Dict[str, Any]:
    """Test the chat endpoint."""
    start_time = time.time()
    try:
        payload = {"message": message, "session_id": f"load_test_{int(time.time())}"}
        async with session.post(f"{base_url}/api/chat", json=payload) as response:
            response_time = time.time() - start_time
            data = await response.json()
            return {
                "success": response.status == 200,
                "response_time": response_time,
                "status_code": response.status,
                "data": data
            }
    except Exception as e:
        return {
            "success": False,
            "response_time": time.time() - start_time,
            "error": str(e)
        }


async def run_concurrent_requests(base_url: str, num_requests: int = 10) -> Dict[str, Any]:
    """Run concurrent requests to test server load handling."""
    print(f"🔥 Running {num_requests} concurrent requests...")
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint concurrency
        print("Testing health endpoint...")
        health_tasks = [
            test_health_endpoint(session, base_url) 
            for _ in range(num_requests)
        ]
        health_results = await asyncio.gather(*health_tasks)
        
        # Test chat endpoint concurrency
        print("Testing chat endpoint...")
        chat_messages = [
            "Hello Jeff!",
            "Can you make pasta?",
            "Tell me about tomatoes",
            "What's your favorite recipe?",
            "How do I cook risotto?"
        ]
        
        chat_tasks = [
            test_chat_endpoint(session, base_url, chat_messages[i % len(chat_messages)])
            for i in range(num_requests)
        ]
        chat_results = await asyncio.gather(*chat_tasks)
        
        return {
            "health_results": health_results,
            "chat_results": chat_results
        }


def analyze_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze load test results."""
    health_results = results["health_results"]
    chat_results = results["chat_results"]
    
    # Health endpoint analysis
    health_success_rate = sum(1 for r in health_results if r["success"]) / len(health_results)
    health_response_times = [r["response_time"] for r in health_results if r["success"]]
    
    # Chat endpoint analysis  
    chat_success_rate = sum(1 for r in chat_results if r["success"]) / len(chat_results)
    chat_response_times = [r["response_time"] for r in chat_results if r["success"]]
    
    analysis = {
        "health_endpoint": {
            "success_rate": round(health_success_rate * 100, 2),
            "avg_response_time": round(statistics.mean(health_response_times) if health_response_times else 0, 3),
            "min_response_time": round(min(health_response_times) if health_response_times else 0, 3),
            "max_response_time": round(max(health_response_times) if health_response_times else 0, 3),
            "total_requests": len(health_results)
        },
        "chat_endpoint": {
            "success_rate": round(chat_success_rate * 100, 2),
            "avg_response_time": round(statistics.mean(chat_response_times) if chat_response_times else 0, 3),
            "min_response_time": round(min(chat_response_times) if chat_response_times else 0, 3),
            "max_response_time": round(max(chat_response_times) if chat_response_times else 0, 3),
            "total_requests": len(chat_results)
        }
    }
    
    return analysis


async def main():
    """Run load tests."""
    base_url = "http://localhost:8000"
    
    print("🍅 Jeff the LangGraph Chef - Load Testing")
    print(f"🎯 Target URL: {base_url}")
    print("="*50)
    
    # Check if server is running
    print("🔍 Checking server availability...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/api/health", timeout=5) as response:
                if response.status == 200:
                    print("✅ Server is running and healthy")
                else:
                    print(f"⚠️  Server responded with status {response.status}")
        except Exception as e:
            print(f"❌ Server not available: {e}")
            print("💡 Start the server with: python scripts/production_server.py")
            return
    
    # Run load tests
    try:
        results = await run_concurrent_requests(base_url, 10)
        analysis = analyze_results(results)
        
        print("\\n📊 Load Test Results:")
        print("="*50)
        
        print("🏥 Health Endpoint:")
        health = analysis["health_endpoint"]
        print(f"  Success Rate: {health['success_rate']}%")
        print(f"  Avg Response: {health['avg_response_time']}s")
        print(f"  Min/Max: {health['min_response_time']}s / {health['max_response_time']}s")
        
        print("\\n💬 Chat Endpoint:")
        chat = analysis["chat_endpoint"]
        print(f"  Success Rate: {chat['success_rate']}%")
        print(f"  Avg Response: {chat['avg_response_time']}s")
        print(f"  Min/Max: {chat['min_response_time']}s / {chat['max_response_time']}s")
        
        # Evaluate against success criteria
        print("\\n🎯 Success Criteria Evaluation:")
        print("="*50)
        
        criteria_met = 0
        total_criteria = 4
        
        if health['success_rate'] >= 95:
            print("✅ Health endpoint success rate ≥95%")
            criteria_met += 1
        else:
            print(f"❌ Health endpoint success rate: {health['success_rate']}% (need ≥95%)")
        
        if chat['success_rate'] >= 90:
            print("✅ Chat endpoint success rate ≥90%")
            criteria_met += 1
        else:
            print(f"❌ Chat endpoint success rate: {chat['success_rate']}% (need ≥90%)")
        
        if chat['avg_response_time'] <= 3.0:
            print("✅ Average response time ≤3.0s")
            criteria_met += 1
        else:
            print(f"❌ Average response time: {chat['avg_response_time']}s (need ≤3.0s)")
        
        if health['avg_response_time'] <= 0.5:
            print("✅ Health check response time ≤0.5s")
            criteria_met += 1
        else:
            print(f"❌ Health check response time: {health['avg_response_time']}s (need ≤0.5s)")
        
        print(f"\\n🏆 Overall Score: {criteria_met}/{total_criteria} criteria met")
        
        if criteria_met == total_criteria:
            print("🎉 All success criteria met! Server is production-ready.")
        else:
            print("⚠️  Some criteria not met. Server needs optimization.")
            
    except Exception as e:
        print(f"❌ Load test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())