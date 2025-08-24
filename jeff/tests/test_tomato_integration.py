"""Tests for Jeff's tomato integration system."""

import pytest
from jeff.personality.tomato_integration import (
    TomatoIntegrationEngine, 
    TomatoIntegrationType,
    TomatoVariety,
    TomatoSuggestion
)
from jeff.personality.models import MoodState


class TestTomatoIntegrationEngine:
    """Test suite for TomatoIntegrationEngine."""
    
    @pytest.fixture
    def tomato_engine(self):
        """Create a TomatoIntegrationEngine instance for testing."""
        return TomatoIntegrationEngine()
    
    def test_engine_initialization(self, tomato_engine):
        """Test that tomato engine initializes correctly."""
        assert len(tomato_engine.tomato_suggestions) > 0
        assert len(tomato_engine.tomato_wisdom) > 0
        assert len(tomato_engine.obsession_phrases) > 0
        assert len(tomato_engine.tomato_pairings) > 0
    
    def test_tomato_suggestion_structure(self, tomato_engine):
        """Test tomato suggestions are properly structured."""
        for suggestion in tomato_engine.tomato_suggestions:
            assert isinstance(suggestion, TomatoSuggestion)
            assert isinstance(suggestion.variety, TomatoVariety)
            assert isinstance(suggestion.integration_type, TomatoIntegrationType)
            assert isinstance(suggestion.description, str)
            assert isinstance(suggestion.romantic_description, str)
            assert 1 <= suggestion.obsession_level_required <= 10
            assert isinstance(suggestion.mood_compatibility, list)
            assert len(suggestion.mood_compatibility) > 0
            assert isinstance(suggestion.dish_compatibility, list)
            assert len(suggestion.dish_compatibility) > 0
    
    def test_obsession_phrases_by_level(self, tomato_engine):
        """Test obsession phrases are organized by intensity level."""
        for level in range(1, 11):
            if level in tomato_engine.obsession_phrases:
                phrases = tomato_engine.obsession_phrases[level]
                assert isinstance(phrases, list)
                assert len(phrases) > 0
                
                for phrase in phrases:
                    assert isinstance(phrase, str)
                    assert len(phrase) > 5  # Should be substantial
    
    def test_tomato_wisdom_categories(self, tomato_engine):
        """Test tomato wisdom categories."""
        required_categories = ["philosophical", "practical", "romantic", "seasonal"]
        
        for category in required_categories:
            assert category in tomato_engine.tomato_wisdom
            wisdom_list = tomato_engine.tomato_wisdom[category]
            assert isinstance(wisdom_list, list)
            assert len(wisdom_list) > 0
            
            for wisdom in wisdom_list:
                assert isinstance(wisdom, str)
                assert len(wisdom) > 20  # Should be meaningful quotes
    
    def test_tomato_pairings_structure(self, tomato_engine):
        """Test tomato pairings structure."""
        required_categories = ["herbs", "proteins", "vegetables", "grains", "dairy", "aromatics"]
        
        for category in required_categories:
            assert category in tomato_engine.tomato_pairings
            ingredients = tomato_engine.tomato_pairings[category]
            assert isinstance(ingredients, list)
            assert len(ingredients) > 0
            
            for ingredient in ingredients:
                assert isinstance(ingredient, str)
                assert len(ingredient) > 0
    
    def test_suggest_tomato_integration_basic(self, tomato_engine):
        """Test basic tomato integration suggestion."""
        suggestion = tomato_engine.suggest_tomato_integration(
            dish_type="pasta",
            existing_ingredients=["garlic", "onion"],
            obsession_level=8,
            current_mood=MoodState.ROMANTIC
        )
        
        # Should return a suggestion for high obsession level with compatible dish
        assert suggestion is not None
        assert isinstance(suggestion, TomatoSuggestion)
        assert suggestion.obsession_level_required <= 8
        assert MoodState.ROMANTIC in suggestion.mood_compatibility or len(suggestion.mood_compatibility) > 2
    
    def test_suggest_tomato_integration_low_obsession(self, tomato_engine):
        """Test tomato integration with low obsession level."""
        suggestion = tomato_engine.suggest_tomato_integration(
            dish_type="dessert",  # Less compatible with tomatoes
            existing_ingredients=["chocolate", "cream"],
            obsession_level=3,
            current_mood=MoodState.SERENE
        )
        
        # Might not suggest anything for low obsession + incompatible dish
        if suggestion:
            assert suggestion.obsession_level_required <= 3
    
    def test_suggest_tomato_integration_with_preference(self, tomato_engine):
        """Test tomato integration with integration type preference."""
        suggestion = tomato_engine.suggest_tomato_integration(
            dish_type="salad",
            existing_ingredients=["lettuce", "cucumber"],
            obsession_level=9,
            current_mood=MoodState.ENTHUSIASTIC,
            integration_preference=TomatoIntegrationType.PRIMARY
        )
        
        if suggestion:
            assert suggestion.integration_type == TomatoIntegrationType.PRIMARY
    
    def test_generate_obsession_comment_levels(self, tomato_engine):
        """Test obsession comment generation at different levels."""
        for level in [3, 6, 8, 10]:
            comment = tomato_engine.generate_tomato_obsession_comment(
                obsession_level=level,
                context="pasta dish",
                mood=MoodState.PASSIONATE
            )
            
            assert isinstance(comment, str)
            assert len(comment) > 10
            # Higher levels should generally produce more intense language
            if level >= 8:
                assert any(intense_word in comment.upper() for intense_word in ["!", "TOMATO", "OBSESS", "PASSION"])
    
    def test_get_tomato_wisdom_categories(self, tomato_engine):
        """Test getting wisdom from different categories."""
        categories = ["philosophical", "practical", "romantic", "seasonal", "random"]
        
        for category in categories:
            wisdom = tomato_engine.get_tomato_wisdom(category)
            assert isinstance(wisdom, str)
            assert len(wisdom) > 15
            # Should contain tomato-related content
            assert "tomato" in wisdom.lower()
    
    def test_analyze_tomato_integration_opportunities(self, tomato_engine):
        """Test analysis of tomato integration opportunities in recipes."""
        recipe_with_tomatoes = "Fresh tomato and basil pasta with garlic and olive oil"
        
        analysis = tomato_engine.analyze_tomato_integration_opportunities(recipe_with_tomatoes)
        
        assert isinstance(analysis, dict)
        assert "current_tomato_presence" in analysis
        assert "integration_opportunities" in analysis
        assert "pairing_synergies" in analysis
        assert "substitution_possibilities" in analysis
        
        # Should detect existing tomatoes
        tomato_presence = analysis["current_tomato_presence"]
        assert tomato_presence["fresh_tomatoes"] == True
        
        # Should find pairing synergies
        synergies = analysis["pairing_synergies"]
        basil_found = any(s["ingredient"] == "basil" for s in synergies)
        garlic_found = any(s["ingredient"] == "garlic" for s in synergies)
        assert basil_found or garlic_found  # Should find at least one
    
    def test_create_tomato_love_declaration(self, tomato_engine):
        """Test tomato love declaration creation."""
        for intensity in [5, 7, 9, 10]:
            declaration = tomato_engine.create_tomato_love_declaration(intensity)
            
            assert isinstance(declaration, str)
            assert len(declaration) > 20
            assert "tomato" in declaration.lower()
            
            # Higher intensity should have more dramatic language
            if intensity >= 9:
                assert any(dramatic in declaration for dramatic in ["!", "OBSESSED", "LIFE", "LOVE"])
    
    def test_seasonal_tomato_approach(self, tomato_engine):
        """Test seasonal tomato approach suggestions."""
        seasons = ["spring", "summer", "fall", "winter"]
        
        for season in seasons:
            approach = tomato_engine.suggest_seasonal_tomato_approach(season)
            
            assert isinstance(approach, str)
            assert len(approach) > 30
            assert season.lower() in approach.lower()
            
            # Summer should be most enthusiastic
            if season == "summer":
                assert any(enthusiastic in approach.upper() for enthusiastic in ["SUMMER", "PEAK", "ABUNDANCE"])
    
    def test_evaluate_tomato_integration_success(self, tomato_engine):
        """Test evaluation of tomato integration success."""
        # High tomato content
        high_tomato_content = "Beautiful ruby tomatoes dance with sun-kissed flavor in this passionate love affair"
        high_score = tomato_engine.evaluate_tomato_integration_success(high_tomato_content, 8)
        
        # Low tomato content
        low_tomato_content = "Cook pasta in water until done"
        low_score = tomato_engine.evaluate_tomato_integration_success(low_tomato_content, 8)
        
        assert 0.0 <= high_score <= 1.0
        assert 0.0 <= low_score <= 1.0
        assert high_score > low_score
    
    def test_synergy_score_calculation(self, tomato_engine):
        """Test calculation of ingredient synergy scores."""
        # Test high-synergy ingredients
        high_synergy_ingredients = ["basil", "mozzarella", "garlic"]
        for ingredient in high_synergy_ingredients:
            score = tomato_engine._calculate_synergy_score(ingredient)
            assert score >= 0.8
        
        # Test medium-synergy ingredients
        medium_synergy_ingredients = ["chicken", "pasta"]
        for ingredient in medium_synergy_ingredients:
            score = tomato_engine._calculate_synergy_score(ingredient)
            assert 0.6 <= score < 0.8
        
        # Test unknown ingredient
        unknown_score = tomato_engine._calculate_synergy_score("unknown_ingredient")
        assert unknown_score == 0.5  # Default score
    
    def test_existing_tomato_detection(self, tomato_engine):
        """Test detection of existing tomatoes in text."""
        test_cases = [
            ("fresh tomato salad", {"fresh_tomatoes": True}),
            ("tomato paste and sauce", {"tomato_products": True}),
            ("sun-dried tomatoes", {"processed_tomatoes": True}),
            ("cherry tomato garnish", {"tomato_varieties": True}),
            ("no tomatoes here", {"fresh_tomatoes": False, "tomato_products": False})
        ]
        
        for text, expected_detections in test_cases:
            detections = tomato_engine._detect_existing_tomatoes(text)
            
            for key, expected_value in expected_detections.items():
                assert detections[key] == expected_value
    
    def test_integration_types_coverage(self):
        """Test that all integration types are covered in suggestions."""
        engine = TomatoIntegrationEngine()
        
        found_types = set()
        for suggestion in engine.tomato_suggestions:
            found_types.add(suggestion.integration_type)
        
        # Should have suggestions for most integration types
        expected_types = {
            TomatoIntegrationType.PRIMARY,
            TomatoIntegrationType.SUPPORTING,
            TomatoIntegrationType.ACCENT,
            TomatoIntegrationType.GARNISH
        }
        
        assert len(found_types.intersection(expected_types)) >= 3  # At least 3 types covered
    
    def test_mood_compatibility_coverage(self):
        """Test that suggestions cover different moods."""
        engine = TomatoIntegrationEngine()
        
        all_moods = set()
        for suggestion in engine.tomato_suggestions:
            all_moods.update(suggestion.mood_compatibility)
        
        # Should cover multiple mood states
        assert len(all_moods) >= 5  # At least 5 different moods
        
        # Should include some key moods
        key_moods = {MoodState.PASSIONATE, MoodState.ROMANTIC, MoodState.ENTHUSIASTIC}
        assert len(all_moods.intersection(key_moods)) >= 2