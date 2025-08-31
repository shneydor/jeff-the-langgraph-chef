#!/usr/bin/env python3
"""Integration tests for Jeff the LangGraph Chef server."""

import pytest
import asyncio
import aiohttp
import json
import time
from typing import Dict, Any


class TestServerIntegration:
    """Integration tests for the FastAPI server."""
    
    BASE_URL = "http://localhost:8000"
    
    @pytest.fixture
    async def session(self):
        """Create aiohttp session for tests."""
        async with aiohttp.ClientSession() as session:
            yield session
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, session):
        """Test health endpoint returns proper status."""
        async with session.get(f"{self.BASE_URL}/api/health") as response:
            assert response.status == 200
            data = await response.json()
            
            assert data["status"] in ["healthy", "unhealthy"]
            assert "timestamp" in data
            assert "service" in data
            assert "version" in data
            assert "metrics" in data
            assert "checks" in data
    
    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, session):
        """Test metrics endpoint returns performance data."""
        async with session.get(f"{self.BASE_URL}/api/metrics") as response:
            assert response.status == 200
            data = await response.json()
            
            assert "uptime_seconds" in data
            assert "requests" in data
            assert "performance" in data
            assert "sessions" in data
            assert "configuration" in data
    
    @pytest.mark.asyncio
    async def test_personality_status_endpoint(self, session):
        """Test personality status endpoint."""
        async with session.get(f"{self.BASE_URL}/api/personality/status") as response:
            assert response.status == 200
            data = await response.json()
            
            assert "tomato_obsession_level" in data
            assert "romantic_intensity" in data
            assert "base_energy_level" in data
            assert "features_enabled" in data
            assert 1 <= data["tomato_obsession_level"] <= 10
            assert 1 <= data["romantic_intensity"] <= 10
    
    @pytest.mark.asyncio
    async def test_chat_endpoint_valid_message(self, session):
        """Test chat endpoint with valid message."""
        payload = {
            "message": "Hello Jeff, can you tell me about tomatoes?",
            "session_id": f"test_session_{int(time.time())}"
        }
        
        start_time = time.time()
        async with session.post(f"{self.BASE_URL}/api/chat", json=payload) as response:
            processing_time = time.time() - start_time
            
            assert response.status == 200
            data = await response.json()
            
            assert data["success"] is True
            assert "response" in data
            assert "metadata" in data
            assert "session_id" in data
            assert len(data["response"]) > 0
            
            # Performance check
            assert processing_time < 10.0  # Allow generous time for first request
    
    @pytest.mark.asyncio
    async def test_chat_endpoint_invalid_message(self, session):
        """Test chat endpoint with invalid message."""
        payload = {"message": ""}  # Empty message
        
        async with session.post(f"{self.BASE_URL}/api/chat", json=payload) as response:
            assert response.status == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_recipe_generation_endpoint(self, session):
        """Test recipe generation endpoint."""
        payload = {
            "recipe_type": "pasta with tomatoes",
            "dietary_restrictions": ["vegetarian"],
            "serving_size": 4,
            "difficulty_level": "medium"
        }
        
        start_time = time.time()
        async with session.post(f"{self.BASE_URL}/api/recipe/generate", json=payload) as response:
            processing_time = time.time() - start_time
            
            assert response.status == 200
            data = await response.json()
            
            assert data["success"] is True
            assert "recipe" in data
            assert "metadata" in data
            assert "request" in data
            assert len(data["recipe"]) > 0
            
            # Verify request echoed back
            assert data["request"]["recipe_type"] == payload["recipe_type"]
            assert data["request"]["serving_size"] == payload["serving_size"]
            
            # Performance check
            assert processing_time < 10.0
    
    @pytest.mark.asyncio
    async def test_demo_scenario_endpoint(self, session):
        """Test demo scenario endpoint."""
        payload = {"scenario": "pasta"}
        
        async with session.post(f"{self.BASE_URL}/api/demo", json=payload) as response:
            assert response.status == 200
            data = await response.json()
            
            assert data["success"] is True
            assert data["scenario"] == "pasta"
            assert "query" in data
            assert "response" in data
            assert len(data["response"]) > 0
    
    @pytest.mark.asyncio
    async def test_demo_invalid_scenario(self, session):
        """Test demo endpoint with invalid scenario."""
        payload = {"scenario": "invalid_scenario"}
        
        async with session.post(f"{self.BASE_URL}/api/demo", json=payload) as response:
            assert response.status == 422  # Validation error


class TestConcurrentRequests:
    """Test server under concurrent load."""
    
    BASE_URL = "http://localhost:8000"
    
    @pytest.mark.asyncio
    async def test_concurrent_health_checks(self):
        """Test multiple concurrent health checks."""
        async with aiohttp.ClientSession() as session:
            tasks = [
                session.get(f"{self.BASE_URL}/api/health")
                for _ in range(10)
            ]
            
            start_time = time.time()
            responses = await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            
            # All requests should succeed
            for response in responses:
                assert response.status == 200
            
            # Should handle 10 concurrent requests quickly
            assert total_time < 5.0
            
            # Close responses
            for response in responses:
                response.close()
    
    @pytest.mark.asyncio
    async def test_concurrent_chat_requests(self):
        """Test multiple concurrent chat requests."""
        async with aiohttp.ClientSession() as session:
            messages = [
                "Hello Jeff!",
                "Tell me about pasta",
                "What's your favorite tomato?",
                "How do I cook risotto?",
                "Give me a recipe"
            ]
            
            tasks = [
                session.post(
                    f"{self.BASE_URL}/api/chat",
                    json={"message": messages[i % len(messages)], "session_id": f"concurrent_test_{i}"}
                )
                for i in range(5)  # Smaller number for chat due to processing time
            ]
            
            start_time = time.time()
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            successful_responses = [r for r in responses if not isinstance(r, Exception)]
            
            # Most requests should succeed (allow some failures under load)
            success_rate = len(successful_responses) / len(responses)
            assert success_rate >= 0.8  # At least 80% success rate
            
            # Should handle concurrent requests reasonably
            assert total_time < 30.0  # Allow generous time for concurrent processing
            
            # Close responses
            for response in successful_responses:
                if hasattr(response, 'close'):
                    response.close()


class TestErrorHandling:
    """Test server error handling capabilities."""
    
    BASE_URL = "http://localhost:8000"
    
    @pytest.mark.asyncio
    async def test_malformed_json(self):
        """Test server handles malformed JSON gracefully."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.BASE_URL}/api/chat",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            ) as response:
                # Should return 422 for validation error or 400 for bad request
                assert response.status in [400, 422]
    
    @pytest.mark.asyncio
    async def test_oversized_message(self):
        """Test server handles oversized messages."""
        async with aiohttp.ClientSession() as session:
            payload = {"message": "x" * 3000}  # Exceeds 2000 char limit
            
            async with session.post(f"{self.BASE_URL}/api/chat", json=payload) as response:
                assert response.status == 422  # Validation error


def test_import_validation():
    """Test that all required modules can be imported."""
    try:
        from jeff.web.app import app
        from jeff.core.config import settings
        from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator
        print("✅ All critical imports successful")
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


if __name__ == "__main__":
    print("🧪 Running Jeff the LangGraph Chef integration tests...")
    print("⚠️  Make sure the server is running on http://localhost:8000")
    print("💡 Start server with: python scripts/production_server.py")
    print()
    
    # Run import validation first
    test_import_validation()
    
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])