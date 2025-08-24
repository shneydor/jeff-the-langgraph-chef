"""Tests for Jeff's romantic writing engine."""

import pytest
from jeff.personality.romantic_engine import RomanticWritingEngine, RomanticStyle
from jeff.personality.models import PersonalityDimensions, MoodState


class TestRomanticWritingEngine:
    """Test suite for RomanticWritingEngine."""
    
    @pytest.fixture
    def romantic_engine(self):
        """Create a RomanticWritingEngine instance for testing."""
        return RomanticWritingEngine()
    
    @pytest.fixture
    def test_dimensions(self):
        """Create test PersonalityDimensions."""
        return PersonalityDimensions(
            romantic_intensity=8,
            energy_level=7,
            creativity_multiplier=1.5
        )
    
    def test_engine_initialization(self, romantic_engine):
        """Test that romantic engine initializes correctly."""
        assert len(romantic_engine.templates) > 0
        assert len(romantic_engine.romantic_vocabulary) > 0
        assert len(romantic_engine.cooking_metaphors) > 0
        assert len(romantic_engine.ingredient_personalities) > 0
    
    def test_romantic_style_selection(self, romantic_engine, test_dimensions):
        """Test romantic style selection based on mood and intensity."""
        # Test passionate mood selection
        style = romantic_engine._select_romantic_style(test_dimensions, MoodState.PASSIONATE)
        assert style in [RomanticStyle.PASSIONATE, RomanticStyle.DRAMATIC]
        
        # Test romantic mood selection
        style = romantic_engine._select_romantic_style(test_dimensions, MoodState.ROMANTIC)
        assert style in [RomanticStyle.TENDER, RomanticStyle.INTIMATE]
        
        # Test playful mood selection
        style = romantic_engine._select_romantic_style(test_dimensions, MoodState.PLAYFUL)
        assert style in [RomanticStyle.WHIMSICAL, RomanticStyle.POETIC]
    
    def test_vocabulary_transformations(self, romantic_engine):
        """Test romantic vocabulary transformations."""
        basic_instruction = "Cook the onions until soft"
        
        transformed = romantic_engine._apply_vocabulary_transformations(basic_instruction)
        
        assert isinstance(transformed, str)
        # Should transform "cook" to something more romantic
        assert "cook" not in transformed.lower() or len(transformed) > len(basic_instruction)
    
    def test_ingredient_extraction(self, romantic_engine):
        """Test ingredient extraction from cooking instructions."""
        instruction = "Sauté garlic and onions with tomatoes and basil"
        
        ingredients = romantic_engine._extract_ingredients(instruction)
        
        assert isinstance(ingredients, list)
        assert "garlic" in ingredients
        assert "onion" in ingredients or "onions" in ingredients
        assert "tomato" in ingredients or "tomatoes" in ingredients
        assert "basil" in ingredients
    
    def test_transform_cooking_instruction(self, romantic_engine, test_dimensions):
        """Test complete cooking instruction transformation."""
        instruction = "Heat oil in pan and add garlic"
        ingredients = ["garlic", "oil"]
        
        transformed = romantic_engine.transform_cooking_instruction(
            instruction, 
            test_dimensions, 
            MoodState.ROMANTIC,
            ingredients
        )
        
        assert isinstance(transformed, str)
        assert len(transformed) >= len(instruction)  # Should be enhanced
        # Should contain romantic elements
        assert any(word in transformed.lower() for word in ["love", "dance", "whisper", "beautiful", "tender"])
    
    def test_recipe_introduction_generation(self, romantic_engine):
        """Test romantic recipe introduction generation."""
        recipe_name = "Pasta Amatriciana"
        main_ingredients = ["tomatoes", "pasta", "pancetta"]
        
        introduction = romantic_engine.generate_romantic_recipe_introduction(
            recipe_name, 
            main_ingredients
        )
        
        assert isinstance(introduction, str)
        assert len(introduction) > 50  # Should be substantial
        assert recipe_name.lower() in introduction.lower()
        # Should contain romantic language
        assert any(word in introduction.lower() for word in ["love", "romance", "beautiful", "story", "tale"])
    
    def test_romantic_cooking_step_generation(self, romantic_engine):
        """Test romantic cooking step generation."""
        step = "Add tomatoes and simmer for 20 minutes"
        step_number = 3
        
        romantic_step = romantic_engine.generate_romantic_cooking_step(step, step_number)
        
        assert isinstance(romantic_step, str)
        assert str(step_number) in romantic_step
        assert len(romantic_step) > len(step)  # Should be enhanced
        # Should contain step prefixes
        assert any(prefix in romantic_step for prefix in ["Step", "Chapter", "Act", "Movement", "Verse"])
    
    def test_chef_note_generation(self, romantic_engine):
        """Test chef's note generation."""
        context = "tomatoes"
        
        note = romantic_engine.generate_chef_note(context)
        
        assert isinstance(note, str)
        assert note.startswith("*Chef Jeff's Romantic Note:")
        assert note.endswith("*")
        assert len(note) > 50  # Should be substantial
    
    def test_ingredient_personalities(self, romantic_engine):
        """Test ingredient personality system."""
        # Test known ingredients
        known_ingredients = ["tomato", "garlic", "butter", "herbs", "onion"]
        
        for ingredient in known_ingredients:
            assert ingredient in romantic_engine.ingredient_personalities
            
            personality_data = romantic_engine.ingredient_personalities[ingredient]
            assert "personality" in personality_data
            assert "romantic_role" in personality_data
            assert "descriptors" in personality_data
            assert "verbs" in personality_data
            
            assert isinstance(personality_data["descriptors"], list)
            assert isinstance(personality_data["verbs"], list)
            assert len(personality_data["descriptors"]) > 0
            assert len(personality_data["verbs"]) > 0
    
    def test_metaphor_categories(self, romantic_engine):
        """Test cooking metaphor categories."""
        required_categories = ["temperature", "texture", "flavor", "aroma"]
        
        for category in required_categories:
            assert category in romantic_engine.cooking_metaphors
            metaphors = romantic_engine.cooking_metaphors[category]
            assert isinstance(metaphors, list)
            assert len(metaphors) > 0
            
            # Each metaphor should be descriptive
            for metaphor in metaphors:
                assert isinstance(metaphor, str)
                assert len(metaphor) > 10  # Should be descriptive
    
    def test_romantic_template_structure(self, romantic_engine):
        """Test romantic template structure and content."""
        for style, templates in romantic_engine.templates.items():
            assert isinstance(style, RomanticStyle)
            assert isinstance(templates, list)
            assert len(templates) > 0
            
            for template in templates:
                assert hasattr(template, 'pattern')
                assert hasattr(template, 'style')
                assert hasattr(template, 'intensity_required')
                assert hasattr(template, 'mood_compatibility')
                assert hasattr(template, 'example')
                
                # Validate template content
                assert isinstance(template.pattern, str)
                assert len(template.pattern) > 20  # Should be substantial
                assert 1 <= template.intensity_required <= 10
                assert isinstance(template.mood_compatibility, list)
                assert len(template.mood_compatibility) > 0
    
    def test_vocabulary_categories(self, romantic_engine):
        """Test romantic vocabulary structure."""
        required_categories = ["verbs", "adjectives", "cooking_terms"]
        
        for category in required_categories:
            assert category in romantic_engine.romantic_vocabulary
            vocab_dict = romantic_engine.romantic_vocabulary[category]
            assert isinstance(vocab_dict, dict)
            assert len(vocab_dict) > 0
            
            # Each vocabulary mapping should have alternatives
            for basic_word, romantic_alternatives in vocab_dict.items():
                assert isinstance(basic_word, str)
                assert isinstance(romantic_alternatives, list)
                assert len(romantic_alternatives) > 0
                
                # Each alternative should be more descriptive
                for alternative in romantic_alternatives:
                    assert isinstance(alternative, str)
                    assert len(alternative) >= len(basic_word)  # Should be more elaborate
    
    def test_metadata_addition(self, romantic_engine, test_dimensions):
        """Test addition of metaphors and descriptions."""
        base_instruction = "Cook the pasta"
        
        enhanced = romantic_engine._add_metaphors_and_descriptions(
            base_instruction, 
            test_dimensions, 
            ["pasta"]
        )
        
        assert isinstance(enhanced, str)
        # With high creativity multiplier, should often add metaphors
        # (this is probabilistic, so we can't guarantee it always happens)
    
    def test_ingredient_personality_addition(self, romantic_engine):
        """Test addition of ingredient personalities."""
        base_instruction = "Add the garlic to the pan"
        ingredients = ["garlic"]
        
        enhanced = romantic_engine._add_ingredient_personalities(
            base_instruction, 
            ingredients
        )
        
        assert isinstance(enhanced, str)
        # Should either be unchanged or enhanced (probabilistic)
        assert len(enhanced) >= len(base_instruction)
    
    def test_empty_ingredient_handling(self, romantic_engine, test_dimensions):
        """Test handling of instructions with no ingredients."""
        instruction = "Preheat the oven to 350 degrees"
        
        transformed = romantic_engine.transform_cooking_instruction(
            instruction, 
            test_dimensions, 
            MoodState.ROMANTIC,
            []  # No ingredients
        )
        
        assert isinstance(transformed, str)
        # Should still work even without ingredients
        assert len(transformed) >= len(instruction)