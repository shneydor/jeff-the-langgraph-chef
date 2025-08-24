"""Tests for Jeff's culinary knowledge base."""

import pytest
from jeff.recipe.knowledge_base import (
    CulinaryKnowledgeBase, 
    Ingredient, 
    CookingMethod,
    FlavorPairing,
    CuisineType,
    DietaryRestriction,
    SkillLevel
)


class TestCulinaryKnowledgeBase:
    """Test suite for CulinaryKnowledgeBase."""
    
    @pytest.fixture
    def knowledge_base(self):
        """Create a CulinaryKnowledgeBase instance for testing."""
        return CulinaryKnowledgeBase()
    
    def test_knowledge_base_initialization(self, knowledge_base):
        """Test that knowledge base initializes with content."""
        assert len(knowledge_base.ingredients) > 0
        assert len(knowledge_base.cooking_methods) > 0
        assert len(knowledge_base.flavor_pairings) > 0
        assert len(knowledge_base.cuisine_knowledge) > 0
        assert len(knowledge_base.dietary_adaptations) > 0
        assert len(knowledge_base.seasonal_guide) > 0
    
    def test_ingredient_structure(self, knowledge_base):
        """Test that ingredients have proper structure."""
        # Test tomato (Jeff's favorite!)
        tomato = knowledge_base.get_ingredient_info("tomato")
        
        assert tomato is not None
        assert isinstance(tomato, Ingredient)
        assert tomato.name == "tomato"
        assert tomato.category == "vegetable"
        assert isinstance(tomato.flavor_profile, list)
        assert len(tomato.flavor_profile) > 0
        assert tomato.jeff_notes is not None
        assert "darling" in tomato.jeff_notes.lower() or "beautiful" in tomato.jeff_notes.lower()
    
    def test_essential_ingredients_present(self, knowledge_base):
        """Test that essential ingredients are in the database."""
        essential_ingredients = [
            "tomato", "cherry_tomato", "garlic", "onion", "basil", 
            "chicken", "mozzarella", "butter", "pasta"
        ]
        
        for ingredient_name in essential_ingredients:
            ingredient = knowledge_base.get_ingredient_info(ingredient_name)
            assert ingredient is not None, f"Missing essential ingredient: {ingredient_name}"
            assert isinstance(ingredient, Ingredient)
            assert ingredient.name == ingredient_name
    
    def test_cooking_methods_structure(self, knowledge_base):
        """Test that cooking methods have proper structure."""
        saute = knowledge_base.get_cooking_method_info("sauté")
        
        assert saute is not None
        assert isinstance(saute, CookingMethod)
        assert saute.name == "sauté"
        assert isinstance(saute.description, str)
        assert len(saute.description) > 20
        assert saute.jeff_wisdom is not None
        assert len(saute.jeff_wisdom) > 20
    
    def test_essential_cooking_methods_present(self, knowledge_base):
        """Test that essential cooking methods are present."""
        essential_methods = ["sauté", "roast", "braise", "blanch"]
        
        for method_name in essential_methods:
            method = knowledge_base.get_cooking_method_info(method_name)
            assert method is not None, f"Missing cooking method: {method_name}"
            assert isinstance(method, CookingMethod)
            assert method.name == method_name
            assert isinstance(method.skill_level, SkillLevel)
    
    def test_flavor_pairings_structure(self, knowledge_base):
        """Test that flavor pairings are properly structured."""
        tomato_pairings = knowledge_base.find_flavor_pairings("tomato")
        
        assert isinstance(tomato_pairings, list)
        assert len(tomato_pairings) > 0
        
        for pairing in tomato_pairings:
            assert isinstance(pairing, FlavorPairing)
            assert pairing.primary_ingredient == "tomato" or pairing.pairing_ingredient == "tomato"
            assert 0.0 <= pairing.synergy_score <= 1.0
            assert isinstance(pairing.cuisine_context, list)
            assert len(pairing.cuisine_context) > 0
    
    def test_tomato_basil_pairing(self, knowledge_base):
        """Test the classic tomato-basil pairing."""
        tomato_pairings = knowledge_base.find_flavor_pairings("tomato")
        
        # Should find tomato-basil pairing
        basil_pairing = None
        for pairing in tomato_pairings:
            if (pairing.primary_ingredient == "tomato" and pairing.pairing_ingredient == "basil") or \
               (pairing.primary_ingredient == "basil" and pairing.pairing_ingredient == "tomato"):
                basil_pairing = pairing
                break
        
        assert basil_pairing is not None, "Should have tomato-basil pairing"
        assert basil_pairing.synergy_score > 0.9  # Should be very high
        assert CuisineType.ITALIAN in basil_pairing.cuisine_context
        assert basil_pairing.jeff_romance is not None
    
    def test_cuisine_knowledge_structure(self, knowledge_base):
        """Test cuisine knowledge structure."""
        italian_cuisine = knowledge_base.get_cuisine_info(CuisineType.ITALIAN)
        
        assert italian_cuisine is not None
        assert isinstance(italian_cuisine, dict)
        assert "core_ingredients" in italian_cuisine
        assert "cooking_techniques" in italian_cuisine
        assert "flavor_principles" in italian_cuisine
        assert "jeff_perspective" in italian_cuisine
        
        # Italian should include tomatoes
        assert "tomato" in italian_cuisine["core_ingredients"]
        assert isinstance(italian_cuisine["jeff_perspective"], str)
        assert len(italian_cuisine["jeff_perspective"]) > 30
    
    def test_dietary_adaptations_structure(self, knowledge_base):
        """Test dietary adaptations structure."""
        vegetarian_info = knowledge_base.get_dietary_adaptations(DietaryRestriction.VEGETARIAN)
        
        assert vegetarian_info is not None
        assert isinstance(vegetarian_info, dict)
        assert "protein_substitutes" in vegetarian_info
        assert "jeff_encouragement" in vegetarian_info
        
        assert isinstance(vegetarian_info["protein_substitutes"], list)
        assert len(vegetarian_info["protein_substitutes"]) > 0
        assert isinstance(vegetarian_info["jeff_encouragement"], str)
    
    def test_seasonal_guide_structure(self, knowledge_base):
        """Test seasonal guide structure."""
        seasons = ["spring", "summer", "fall", "winter"]
        
        for season in seasons:
            seasonal_info = knowledge_base.get_seasonal_ingredients(season)
            assert isinstance(seasonal_info, dict)
            
            if seasonal_info:  # Not all seasons may have info
                assert "vegetables" in seasonal_info or "herbs" in seasonal_info
                assert "jeff_mood" in seasonal_info
                assert isinstance(seasonal_info["jeff_mood"], str)
        
        # Summer should definitely have tomatoes
        summer_info = knowledge_base.get_seasonal_ingredients("summer")
        if summer_info and "vegetables" in summer_info:
            assert "tomatoes" in summer_info["vegetables"]
    
    def test_ingredient_substitutions(self, knowledge_base):
        """Test ingredient substitution suggestions."""
        tomato_subs = knowledge_base.suggest_substitutions("tomato")
        
        assert isinstance(tomato_subs, list)
        if len(tomato_subs) > 0:  # May not have substitutions
            for sub in tomato_subs:
                assert isinstance(sub, str)
                assert len(sub) > 0
    
    def test_find_ingredients_by_category(self, knowledge_base):
        """Test finding ingredients by category."""
        vegetables = knowledge_base.find_ingredients_by_category("vegetable")
        
        assert isinstance(vegetables, list)
        assert len(vegetables) > 0
        assert "tomato" in vegetables  # Jeff's favorite should be there
        
        # Test other categories
        proteins = knowledge_base.find_ingredients_by_category("protein")
        dairy = knowledge_base.find_ingredients_by_category("dairy")
        
        assert isinstance(proteins, list)
        assert isinstance(dairy, list)
    
    def test_jeff_wisdom_retrieval(self, knowledge_base):
        """Test Jeff's wisdom retrieval."""
        # Test cooking method wisdom
        saute_wisdom = knowledge_base.get_jeff_wisdom("sauté")
        assert saute_wisdom is not None
        assert isinstance(saute_wisdom, str)
        assert len(saute_wisdom) > 20
        
        # Test ingredient wisdom
        tomato_wisdom = knowledge_base.get_jeff_wisdom("tomato")
        assert tomato_wisdom is not None
        assert isinstance(tomato_wisdom, str)
        assert "tomato" in tomato_wisdom.lower()
        
        # Test unknown topic
        unknown_wisdom = knowledge_base.get_jeff_wisdom("nonexistent_topic")
        # May return None or a default response
    
    def test_knowledge_search(self, knowledge_base):
        """Test knowledge search functionality."""
        # Search for tomato-related content
        results = knowledge_base.search_knowledge("tomato")
        
        assert isinstance(results, dict)
        assert "ingredients" in results
        assert "cooking_methods" in results
        assert "pairings" in results
        assert "cuisines" in results
        
        # Should find tomato ingredient
        assert len(results["ingredients"]) > 0
        tomato_found = any(ing.name == "tomato" for ing in results["ingredients"])
        assert tomato_found
        
        # Should find tomato pairings
        assert len(results["pairings"]) > 0
    
    def test_ingredient_common_pairings(self, knowledge_base):
        """Test that ingredients have meaningful common pairings."""
        tomato = knowledge_base.get_ingredient_info("tomato")
        
        assert tomato.common_pairings is not None
        assert isinstance(tomato.common_pairings, list)
        assert len(tomato.common_pairings) > 0
        
        # Should include classic pairings
        classic_pairings = ["basil", "mozzarella", "garlic", "olive_oil"]
        found_classics = [p for p in classic_pairings if p in tomato.common_pairings]
        assert len(found_classics) >= 2  # Should have at least 2 classic pairings
    
    def test_cooking_method_equipment_and_tips(self, knowledge_base):
        """Test that cooking methods have equipment and tips."""
        saute = knowledge_base.get_cooking_method_info("sauté")
        
        assert saute.equipment_needed is not None
        assert isinstance(saute.equipment_needed, list)
        assert len(saute.equipment_needed) > 0
        assert "skillet" in saute.equipment_needed or "pan" in saute.equipment_needed
        
        assert saute.tips is not None
        assert isinstance(saute.tips, list)
        assert len(saute.tips) > 0
        
        assert saute.common_mistakes is not None
        assert isinstance(saute.common_mistakes, list)
    
    def test_ingredient_nutritional_highlights(self, knowledge_base):
        """Test that key ingredients have nutritional information."""
        tomato = knowledge_base.get_ingredient_info("tomato")
        
        assert tomato.nutritional_highlights is not None
        assert isinstance(tomato.nutritional_highlights, list)
        assert len(tomato.nutritional_highlights) > 0
        
        # Tomatoes should highlight lycopene
        assert "lycopene" in tomato.nutritional_highlights
    
    def test_ingredient_storage_and_prep(self, knowledge_base):
        """Test that ingredients have storage and prep information."""
        tomato = knowledge_base.get_ingredient_info("tomato")
        
        assert tomato.storage_method is not None
        assert isinstance(tomato.storage_method, str)
        
        assert tomato.prep_notes is not None
        assert isinstance(tomato.prep_notes, str)
        # Should mention not refrigerating
        assert "refrigerat" in tomato.prep_notes.lower()
    
    def test_seasonal_consistency(self, knowledge_base):
        """Test seasonal information consistency."""
        # Summer should be tomato season
        summer = knowledge_base.get_seasonal_ingredients("summer")
        assert summer is not None
        assert "vegetables" in summer
        assert "tomatoes" in summer["vegetables"]
        
        # Jeff should be most excited about summer
        assert "jeff_mood" in summer
        jeff_summer_mood = summer["jeff_mood"].lower()
        assert any(word in jeff_summer_mood for word in ["magic", "perfect", "peak", "beloved"])
    
    def test_case_insensitive_lookups(self, knowledge_base):
        """Test that lookups are case insensitive."""
        # Test different cases
        tomato_lower = knowledge_base.get_ingredient_info("tomato")
        tomato_upper = knowledge_base.get_ingredient_info("TOMATO")
        tomato_mixed = knowledge_base.get_ingredient_info("Tomato")
        
        assert tomato_lower is not None
        assert tomato_upper is not None  
        assert tomato_mixed is not None
        
        # Should all return same ingredient
        assert tomato_lower.name == tomato_upper.name == tomato_mixed.name