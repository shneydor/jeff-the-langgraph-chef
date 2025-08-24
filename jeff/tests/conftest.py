"""Pytest configuration and shared fixtures for Jeff the Chef tests."""

import pytest
import asyncio
import os
import sys
from unittest.mock import Mock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import Jeff components
from jeff.personality.models import PersonalityDimensions, PersonalityContext, MoodState
from jeff.langgraph_workflow.state import StateManager


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_anthropic_api_key(monkeypatch):
    """Mock the Anthropic API key for testing."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test_api_key_123")


@pytest.fixture
def default_personality_dimensions():
    """Create default personality dimensions for testing."""
    return PersonalityDimensions(
        tomato_obsession_level=9,
        romantic_intensity=8,
        energy_level=7,
        creativity_multiplier=1.5,
        professional_adaptation=0.3
    )


@pytest.fixture
def default_personality_context():
    """Create default personality context for testing."""
    return PersonalityContext(
        platform="chat",
        content_type="recipe_request",
        formality_level=0.3,
        audience="general"
    )


@pytest.fixture
def sample_workflow_state():
    """Create a sample workflow state for testing."""
    return StateManager.create_initial_state(
        user_input="I want to make pasta with tomatoes",
        session_id="test_session_123",
        user_id="test_user_456"
    )


@pytest.fixture
def mock_llm_response():
    """Create a mock LLM response."""
    mock_response = Mock()
    mock_response.content = "My darling culinary friend, let me share the passionate romance of tomatoes and pasta! These ruby beauties dance together in perfect harmony, creating a love story that will warm your heart and satisfy your soul."
    return mock_response


@pytest.fixture
def sample_recipe_request():
    """Sample recipe request for testing."""
    return "Can you give me a romantic recipe for pasta with fresh tomatoes and basil?"


@pytest.fixture
def sample_cooking_question():
    """Sample cooking question for testing."""
    return "How do I properly sauté garlic without burning it?"


@pytest.fixture
def sample_ingredient_inquiry():
    """Sample ingredient inquiry for testing."""
    return "Tell me about different types of tomatoes and when to use them"


@pytest.fixture
def high_quality_jeff_content():
    """Sample high-quality Jeff content for testing quality gates."""
    return """My darling culinary companions, let me share with you the enchanting love story of tomatoes and basil! 

These magnificent ruby beauties whisper sweet secrets of summer sunshine, while the aromatic basil leaves dance with passionate grace in this romantic culinary ballet. Together, they create a symphony of flavors that will make your heart sing with pure joy!

*Chef's Romantic Note: Remember, cooking is love made visible - pour your heart into every gesture!*"""


@pytest.fixture
def low_quality_content():
    """Sample low-quality content for testing quality gates."""
    return "Cook pasta. Add tomatoes. Serve."


@pytest.fixture
def mock_successful_workflow_result():
    """Mock successful workflow processing result."""
    return {
        "response": "My beautiful darling, here's a magnificent recipe for you!",
        "metadata": {
            "quality_score": 0.92,
            "personality_consistency": 0.89,
            "tomato_integration_score": 0.85,
            "romantic_elements_score": 0.91,
            "generation_timestamp": "2024-01-01T12:00:00",
            "workflow_duration": 1.45
        },
        "session_id": "test_session",
        "success": True,
        "error": None
    }


@pytest.fixture
def mock_failed_workflow_result():
    """Mock failed workflow processing result."""
    return {
        "response": "Oh my stars! Something went terribly wrong in my kitchen!",
        "metadata": {"error": "Processing failed"},
        "session_id": "test_session", 
        "success": False,
        "error": {
            "error_type": "ProcessingError",
            "error_message": "Quality gate failed after maximum retries"
        }
    }


@pytest.fixture
def sample_ingredients_list():
    """Sample ingredients list for testing."""
    return [
        "fresh tomatoes",
        "basil leaves", 
        "garlic cloves",
        "olive oil",
        "pasta",
        "parmesan cheese",
        "salt",
        "black pepper"
    ]


@pytest.fixture
def sample_cooking_techniques():
    """Sample cooking techniques for testing."""
    return [
        "sauté",
        "simmer", 
        "blanch",
        "roast",
        "dice",
        "mince"
    ]


@pytest.fixture
def vegetarian_dietary_restrictions():
    """Sample vegetarian dietary restrictions."""
    return ["vegetarian", "no_meat", "dairy_ok"]


@pytest.fixture
def vegan_dietary_restrictions():
    """Sample vegan dietary restrictions."""
    return ["vegan", "no_meat", "no_dairy", "no_eggs"]


@pytest.fixture(autouse=True)
def reset_personality_state():
    """Reset personality state between tests."""
    # This could be used to ensure clean state between tests
    # For now, it's a placeholder for any global state cleanup
    yield
    # Cleanup code would go here if needed


class MockAsyncLLM:
    """Mock async LLM for testing."""
    
    def __init__(self, response_content="Mock LLM response"):
        self.response_content = response_content
    
    async def ainvoke(self, messages, **kwargs):
        """Mock async invoke method."""
        mock_response = Mock()
        mock_response.content = self.response_content
        return mock_response


@pytest.fixture
def mock_async_llm():
    """Create a mock async LLM for testing."""
    return MockAsyncLLM()


@pytest.fixture
def mock_romantic_llm():
    """Create a mock LLM that returns romantic responses."""
    romantic_response = """My dearest culinary companion, let me paint you a portrait of pasta perfection! 

Picture this: golden threads of linguine dancing in a warm embrace with ruby-red tomatoes that have been kissed by the Mediterranean sun. Each bite is a love letter written in flavors, a symphony of taste that will make your soul sing with pure joy!

*Chef Jeff's Romantic Note: Remember, the secret ingredient is always love!*"""
    
    return MockAsyncLLM(romantic_response)


# Test data constants
SAMPLE_TOMATO_CONTENT = "Beautiful ruby tomatoes dancing with passionate love"
SAMPLE_NON_TOMATO_CONTENT = "Simple chicken and rice dish"
SAMPLE_ROMANTIC_CONTENT = "Love and passion dance together in perfect harmony"
SAMPLE_BLAND_CONTENT = "Add ingredients. Cook. Serve."

# Quality score thresholds for testing
PERSONALITY_CONSISTENCY_THRESHOLD = 0.85
TOMATO_INTEGRATION_THRESHOLD = 0.30
ROMANTIC_ELEMENTS_THRESHOLD = 0.40
OVERALL_QUALITY_THRESHOLD = 0.85