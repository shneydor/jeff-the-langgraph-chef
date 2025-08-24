"""Tests for Jeff's personality engine."""

import pytest
import asyncio
from unittest.mock import Mock, patch

from jeff.personality.engine import PersonalityEngine
from jeff.personality.models import (
    PersonalityDimensions, 
    PersonalityContext, 
    MoodState,
    PersonalityConfig
)


class TestPersonalityEngine:
    """Test suite for PersonalityEngine."""
    
    @pytest.fixture
    def personality_engine(self):
        """Create a PersonalityEngine instance for testing."""
        return PersonalityEngine()
    
    @pytest.fixture
    def test_context(self):
        """Create a test PersonalityContext."""
        return PersonalityContext(
            platform="chat",
            content_type="recipe_request",
            formality_level=0.3
        )
    
    @pytest.mark.asyncio
    async def test_personality_engine_initialization(self, personality_engine):
        """Test that personality engine initializes correctly."""
        assert personality_engine.config is not None
        assert personality_engine._state is not None
        assert len(personality_engine._mood_triggers) > 0
        assert len(personality_engine._personality_templates) > 0
    
    @pytest.mark.asyncio
    async def test_process_input_basic(self, personality_engine, test_context):
        """Test basic input processing."""
        response = await personality_engine.process_input(
            "I want to make pasta with tomatoes", 
            test_context
        )
        
        assert response is not None
        assert response.content != ""
        assert 0.0 <= response.consistency_score <= 1.0
        assert 0.0 <= response.tomato_integration_score <= 1.0
        assert isinstance(response.romantic_elements, list)
    
    @pytest.mark.asyncio
    async def test_mood_update_from_input(self, personality_engine):
        """Test that mood updates based on input content."""
        initial_mood = personality_engine._state.current_mood
        
        # Test input with tomato triggers (should trigger ecstatic mood)
        await personality_engine._update_mood_from_input("I love tomatoes! They're perfect!")
        
        # Mood might change (depending on mood stability)
        new_mood = personality_engine._state.current_mood
        assert isinstance(new_mood, MoodState)
    
    @pytest.mark.asyncio
    async def test_personality_transformation(self, personality_engine):
        """Test personality transformation of content."""
        base_content = "Cook the pasta in boiling water."
        
        transformed = await personality_engine._apply_personality_transformation(base_content)
        
        assert transformed != base_content  # Should be transformed
        assert len(transformed) >= len(base_content)  # Should be enhanced
    
    @pytest.mark.asyncio
    async def test_consistency_scoring(self, personality_engine):
        """Test personality consistency scoring."""
        # Test with Jeff-like content
        jeff_content = "My darling tomatoes whisper sweet secrets of love in this magnificent pasta!"
        score = await personality_engine._calculate_consistency_score(jeff_content)
        
        assert 0.0 <= score <= 1.0
        assert score > 0.5  # Should score well for Jeff-like content
        
        # Test with non-Jeff content
        bland_content = "Add water to pot. Boil."
        bland_score = await personality_engine._calculate_consistency_score(bland_content)
        
        assert bland_score < score  # Should score lower
    
    def test_tomato_integration_scoring(self, personality_engine):
        """Test tomato integration scoring."""
        # Content with tomatoes
        tomato_content = "Beautiful ruby tomatoes dancing in olive oil"
        tomato_score = personality_engine._calculate_tomato_integration_score(tomato_content)
        
        assert tomato_score > 0.0
        
        # Content without tomatoes
        no_tomato_content = "Boil pasta in water"
        no_tomato_score = personality_engine._calculate_tomato_integration_score(no_tomato_content)
        
        assert tomato_score > no_tomato_score
    
    def test_romantic_elements_extraction(self, personality_engine):
        """Test extraction of romantic elements."""
        romantic_content = "The love between basil and tomatoes creates a beautiful dance of passion"
        elements = personality_engine._extract_romantic_elements(romantic_content)
        
        assert isinstance(elements, list)
        assert "love" in elements
        assert "beautiful" in elements
        assert "passion" in elements
    
    def test_personality_dimensions_update(self, personality_engine):
        """Test updating personality dimensions."""
        new_dimensions = PersonalityDimensions(
            tomato_obsession_level=10,
            romantic_intensity=10,
            energy_level=10
        )
        
        personality_engine.update_dimensions(new_dimensions)
        
        assert personality_engine._state.dimensions.tomato_obsession_level == 10
        assert personality_engine._state.dimensions.romantic_intensity == 10
        assert personality_engine._state.dimensions.energy_level == 10
    
    def test_consistency_stats(self, personality_engine):
        """Test consistency statistics tracking."""
        # Add some consistency scores
        personality_engine._consistency_history = [0.8, 0.9, 0.85, 0.95]
        
        stats = personality_engine.get_consistency_stats()
        
        assert "average" in stats
        assert "recent" in stats
        assert "trend" in stats
        assert 0.0 <= stats["average"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_mood_specific_transformations(self, personality_engine):
        """Test mood-specific content transformations."""
        content = "Cook the vegetables"
        
        # Test different mood transformations
        moods_to_test = [
            MoodState.ECSTATIC,
            MoodState.ROMANTIC,
            MoodState.PASSIONATE,
            MoodState.CONTEMPLATIVE
        ]
        
        for mood in moods_to_test:
            personality_engine._state.current_mood = mood
            transformed = await personality_engine._apply_mood_transformation(content)
            
            assert isinstance(transformed, str)
            # Each mood should transform differently
            assert len(transformed) >= len(content)
    
    @pytest.mark.asyncio
    async def test_platform_adaptations(self, personality_engine):
        """Test platform-specific adaptations."""
        content = "I absolutely love cooking with tomatoes! They make everything magnificent and wonderful!"
        
        # Test Twitter adaptation (should shorten)
        personality_engine._state.context = PersonalityContext(platform="twitter")
        twitter_adapted = await personality_engine._adapt_for_twitter(content)
        
        assert len(twitter_adapted) <= 280  # Twitter character limit
        
        # Test LinkedIn adaptation (should be more professional)
        linkedin_adapted = await personality_engine._adapt_for_linkedin(content)
        
        assert "As a culinary professional" in linkedin_adapted
    
    def test_configuration_loading(self):
        """Test personality configuration loading."""
        config = PersonalityConfig(
            min_consistency_score=0.95,
            regeneration_threshold=0.90,
            mood_stability=0.8
        )
        
        engine = PersonalityEngine(config)
        
        assert engine.config.min_consistency_score == 0.95
        assert engine.config.regeneration_threshold == 0.90
        assert engine.config.mood_stability == 0.8