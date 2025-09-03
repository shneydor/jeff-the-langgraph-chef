"""Tomato integration system for Jeff's obsessive love of tomatoes."""

import random
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass

from .models import PersonalityDimensions, MoodState


class TomatoIntegrationType(str, Enum):
    """Types of tomato integration strategies."""
    PRIMARY = "primary"          # Tomato as main ingredient
    SUPPORTING = "supporting"    # Tomato as complementary ingredient
    ACCENT = "accent"           # Small amount for flavor enhancement
    GARNISH = "garnish"         # Visual and flavor accent
    SUBSTITUTE = "substitute"   # Creative replacement suggestion
    INSPIRED = "inspired"       # Tomato-inspired element without actual tomatoes


class TomatoVariety(str, Enum):
    """Different tomato varieties Jeff can suggest."""
    CHERRY = "cherry tomatoes"
    ROMA = "roma tomatoes" 
    BEEFSTEAK = "beefsteak tomatoes"
    HEIRLOOM = "heirloom tomatoes"
    SUN_DRIED = "sun-dried tomatoes"
    PASTE = "tomato paste"
    SAUCE = "tomato sauce"
    PUREE = "tomato puree"
    FRESH = "fresh tomatoes"
    CANNED = "canned tomatoes"
    ROASTED = "roasted tomatoes"


@dataclass
class TomatoSuggestion:
    """A tomato integration suggestion."""
    variety: TomatoVariety
    integration_type: TomatoIntegrationType
    description: str
    romantic_description: str
    obsession_level_required: int  # 1-10
    mood_compatibility: List[MoodState]
    dish_compatibility: List[str]  # Types of dishes this works with
    preparation_note: Optional[str] = None


class TomatoIntegrationEngine:
    """Engine for integrating Jeff's tomato obsession into recipes and content."""
    
    def __init__(self):
        self.tomato_suggestions = self._initialize_tomato_suggestions()
        self.tomato_wisdom = self._initialize_tomato_wisdom()
        self.obsession_phrases = self._initialize_obsession_phrases()
        self.tomato_pairings = self._initialize_tomato_pairings()
        
    def _initialize_tomato_suggestions(self) -> List[TomatoSuggestion]:
        """Initialize comprehensive tomato integration suggestions."""
        return [
            # Primary Integration
            TomatoSuggestion(
                variety=TomatoVariety.HEIRLOOM,
                integration_type=TomatoIntegrationType.PRIMARY,
                description="Feature beautiful heirloom tomatoes as the star of the dish",
                romantic_description="Let these magnificent heirloom beauties steal the spotlight with their rainbow of colors and symphony of flavors",
                obsession_level_required=8,
                mood_compatibility=[MoodState.ECSTATIC, MoodState.PASSIONATE, MoodState.ROMANTIC],
                dish_compatibility=["salad", "caprese", "bruschetta", "pasta"],
                preparation_note="Slice thick to showcase their natural beauty"
            ),
            TomatoSuggestion(
                variety=TomatoVariety.SUN_DRIED,
                integration_type=TomatoIntegrationType.SUPPORTING,
                description="Add sun-dried tomatoes for concentrated flavor",
                romantic_description="These sun-kissed gems have captured summer's essence in every wrinkled, flavor-packed morsel",
                obsession_level_required=6,
                mood_compatibility=[MoodState.CONTEMPLATIVE, MoodState.NOSTALGIC, MoodState.ROMANTIC],
                dish_compatibility=["pasta", "pizza", "chicken", "salad", "bread"],
                preparation_note="Rehydrate in warm wine for extra romance"
            ),
            TomatoSuggestion(
                variety=TomatoVariety.CHERRY,
                integration_type=TomatoIntegrationType.ACCENT,
                description="Burst cherry tomatoes for pops of flavor and color",
                romantic_description="These little ruby jewels will burst like tiny fireworks of joy on your tongue",
                obsession_level_required=5,
                mood_compatibility=[MoodState.PLAYFUL, MoodState.ENTHUSIASTIC, MoodState.MISCHIEVOUS],
                dish_compatibility=["pasta", "salad", "roasted vegetables", "grain bowls"],
                preparation_note="Blister them whole for maximum impact"
            ),
            
            # Creative Substitutions
            TomatoSuggestion(
                variety=TomatoVariety.PASTE,
                integration_type=TomatoIntegrationType.SUBSTITUTE,
                description="Use tomato paste to add umami depth to unexpected dishes",
                romantic_description="This concentrated love potion can transform any dish into a passionate affair",
                obsession_level_required=9,
                mood_compatibility=[MoodState.PASSIONATE, MoodState.INSPIRED, MoodState.MISCHIEVOUS],
                dish_compatibility=["stew", "marinade", "soup", "sauce", "curry"],
                preparation_note="Bloom in oil first to develop complex flavors"
            ),
            
            # Garnish Ideas
            TomatoSuggestion(
                variety=TomatoVariety.FRESH,
                integration_type=TomatoIntegrationType.GARNISH,
                description="Fresh tomato microgreens or baby tomatoes as elegant garnish",
                romantic_description="Like scattered rose petals, these delicate beauties add the perfect finishing touch",
                obsession_level_required=7,
                mood_compatibility=[MoodState.SERENE, MoodState.ROMANTIC, MoodState.INSPIRED],
                dish_compatibility=["fine dining", "appetizers", "soup", "salad"],
                preparation_note="Choose the most perfect specimens for visual impact"
            ),
            
            # Inspired Integration (no actual tomatoes)
            TomatoSuggestion(
                variety=TomatoVariety.FRESH,  # Conceptual
                integration_type=TomatoIntegrationType.INSPIRED,
                description="Tomato-inspired color and acidity through other red ingredients",
                romantic_description="Channel the spirit of my beloved tomatoes through ruby red beets, pomegranate, or red bell peppers",
                obsession_level_required=10,
                mood_compatibility=[MoodState.INSPIRED, MoodState.CONTEMPLATIVE, MoodState.PASSIONATE],
                dish_compatibility=["any dish"],
                preparation_note="Think tomato essence without the tomato"
            )
        ]
    
    def _initialize_tomato_wisdom(self) -> Dict[str, List[str]]:
        """Initialize tomato-related wisdom and quotes."""
        return {
            "philosophical": [
                "A tomato is not just a fruit, it's a love letter from the earth to our souls",
                "In every tomato lies the secret to happiness - you just have to know how to listen",
                "The tomato teaches us that the most beautiful things come from humble beginnings",
                "Life is like a tomato - it's all about timing, sunshine, and a little bit of magic"
            ],
            "practical": [
                "Never refrigerate a tomato unless you want to break its heart and yours",
                "The secret to perfect tomatoes is patience - let them ripen on the vine of life",
                "A tomato's shoulders tell its story - look for green shoulders on the most flavorful ones",
                "Salt your tomatoes and wait - they'll reward your patience with concentrated love"
            ],
            "romantic": [
                "Tomatoes are the cupid of the vegetable world - they make everything fall in love",
                "In Italy, they say tomatoes are kisses from the Mediterranean sun",
                "A perfect tomato is like finding true love - you know it the moment you taste it",
                "Tomatoes don't just grow in gardens, they bloom in the heart of every great chef"
            ],
            "seasonal": [
                "Summer tomatoes are love songs, winter tomatoes are gentle lullabies",
                "In spring, I dream of tomatoes; in summer, I dance with them",
                "Autumn tomatoes carry the wisdom of the full season in their ruby depths",
                "Even in winter, tomatoes remind us that sunshine lives in a can"
            ]
        }
    
    def _initialize_obsession_phrases(self) -> Dict[int, List[str]]:
        """Initialize obsession-level appropriate phrases."""
        return {
            # Mild obsession (1-3)
            1: ["Perhaps a touch of tomato?", "Tomatoes might be nice here"],
            2: ["I can't help but think tomatoes would elevate this", "My heart whispers 'tomatoes'"],
            3: ["Surely tomatoes would make this even better!", "I'm drawn to add tomatoes"],
            
            # Moderate obsession (4-6)
            4: ["My beloved tomatoes are calling to join this dish!", "I simply must suggest tomatoes"],
            5: ["Oh, how my heart sings at the thought of tomatoes here!", "Tomatoes would make this absolutely divine!"],
            6: ["I'm practically trembling with the need to add tomatoes!", "My tomato-loving soul demands their inclusion!"],
            
            # High obsession (7-8)
            7: ["I cannot contain my excitement about adding tomatoes!", "My darling tomatoes MUST be part of this romance!"],
            8: ["Every fiber of my being screams for tomatoes in this dish!", "I'm literally vibrating with tomato passion!"],
            
            # Extreme obsession (9-10)
            9: ["I am OBSESSED with the idea of tomatoes in this creation!", "My tomato devotion borders on the spiritual!"],
            10: ["TOMATOES! TOMATOES! They must unite with this dish in holy matrimony!", "I am one with the tomato universe!"]
        }
    
    def _initialize_tomato_pairings(self) -> Dict[str, List[str]]:
        """Initialize tomato pairing suggestions for different ingredient categories."""
        return {
            "herbs": ["basil", "oregano", "thyme", "rosemary", "parsley", "cilantro"],
            "proteins": ["chicken", "beef", "pork", "fish", "eggs", "cheese", "beans"],
            "vegetables": ["onions", "garlic", "peppers", "eggplant", "zucchini", "mushrooms"],
            "grains": ["pasta", "rice", "quinoa", "bread", "polenta", "couscous"],
            "dairy": ["mozzarella", "parmesan", "ricotta", "cream", "butter", "goat cheese"],
            "aromatics": ["wine", "vinegar", "lemon", "lime", "capers", "olives"]
        }
    
    def suggest_tomato_integration(
        self, 
        dish_type: str,
        existing_ingredients: List[str],
        obsession_level: int,
        current_mood: MoodState,
        integration_preference: Optional[TomatoIntegrationType] = None
    ) -> Optional[TomatoSuggestion]:
        """Suggest appropriate tomato integration for a dish."""
        
        # Filter suggestions by compatibility
        compatible_suggestions = []
        
        for suggestion in self.tomato_suggestions:
            # Check obsession level requirement
            if suggestion.obsession_level_required <= obsession_level:
                # Check mood compatibility
                if current_mood in suggestion.mood_compatibility:
                    # Check dish compatibility
                    if any(dish_type.lower() in dish.lower() or dish.lower() in dish_type.lower() 
                          for dish in suggestion.dish_compatibility):
                        # Check integration type preference
                        if integration_preference is None or suggestion.integration_type == integration_preference:
                            compatible_suggestions.append(suggestion)
        
        # If no compatible suggestions, try with relaxed criteria
        if not compatible_suggestions and obsession_level >= 8:
            # For high obsession, be more flexible
            compatible_suggestions = [s for s in self.tomato_suggestions 
                                    if s.obsession_level_required <= obsession_level + 2]
        
        return random.choice(compatible_suggestions) if compatible_suggestions else None
    
    def generate_tomato_obsession_comment(
        self, 
        obsession_level: int, 
        context: str = "", 
        mood: MoodState = MoodState.ENTHUSIASTIC
    ) -> str:
        """Generate an obsession-appropriate tomato comment."""
        
        # Get phrases for obsession level
        level_phrases = []
        for level in range(1, obsession_level + 1):
            level_phrases.extend(self.obsession_phrases.get(level, []))
        
        if not level_phrases:
            level_phrases = self.obsession_phrases.get(5, ["Tomatoes would be wonderful here!"])
        
        base_phrase = random.choice(level_phrases)
        
        # Add context-specific enhancement
        if context:
            enhancements = [
                f"Imagine {context} enhanced by the ruby magic of tomatoes!",
                f"Picture how tomatoes would dance with {context} in perfect harmony!",
                f"The combination of {context} and tomatoes would be pure poetry!",
                f"My heart races thinking of {context} united with beautiful tomatoes!"
            ]
            enhancement = random.choice(enhancements)
            return f"{base_phrase} {enhancement}"
        
        return base_phrase
    
    def get_tomato_wisdom(self, category: str = "random") -> str:
        """Get tomato wisdom quote from specified category."""
        if category == "random":
            all_wisdom = []
            for wisdom_list in self.tomato_wisdom.values():
                all_wisdom.extend(wisdom_list)
            return random.choice(all_wisdom)
        
        wisdom_list = self.tomato_wisdom.get(category, self.tomato_wisdom["practical"])
        return random.choice(wisdom_list)
    
    def analyze_tomato_integration_opportunities(self, recipe_text: str) -> Dict[str, Any]:
        """Analyze a recipe for tomato integration opportunities."""
        text_lower = recipe_text.lower()
        
        opportunities = {
            "current_tomato_presence": self._detect_existing_tomatoes(text_lower),
            "integration_opportunities": [],
            "pairing_synergies": [],
            "substitution_possibilities": []
        }
        
        # Find integration opportunities
        for ingredient_category, ingredients in self.tomato_pairings.items():
            for ingredient in ingredients:
                if ingredient in text_lower:
                    opportunities["pairing_synergies"].append({
                        "ingredient": ingredient,
                        "category": ingredient_category,
                        "synergy_score": self._calculate_synergy_score(ingredient)
                    })
        
        # Suggest integration types based on dish analysis
        if "salad" in text_lower:
            opportunities["integration_opportunities"].append(TomatoIntegrationType.PRIMARY)
        if "pasta" in text_lower or "sauce" in text_lower:
            opportunities["integration_opportunities"].append(TomatoIntegrationType.SUPPORTING)
        if "garnish" in text_lower or "finish" in text_lower:
            opportunities["integration_opportunities"].append(TomatoIntegrationType.GARNISH)
        
        return opportunities
    
    def _detect_existing_tomatoes(self, text: str) -> Dict[str, bool]:
        """Detect existing tomato presence in text."""
        tomato_indicators = {
            "fresh_tomatoes": any(term in text for term in ["fresh tomato", "ripe tomato", "tomato"]),
            "tomato_products": any(term in text for term in ["tomato paste", "tomato sauce", "tomato puree"]),
            "processed_tomatoes": any(term in text for term in ["canned tomato", "sun-dried", "roasted tomato"]),
            "tomato_varieties": any(term in text for term in ["cherry tomato", "roma", "beefsteak", "heirloom"])
        }
        
        return tomato_indicators
    
    def _calculate_synergy_score(self, ingredient: str) -> float:
        """Calculate how well an ingredient pairs with tomatoes."""
        # Classic high-synergy ingredients
        high_synergy = ["basil", "mozzarella", "garlic", "onion", "oregano", "olive oil"]
        medium_synergy = ["chicken", "pasta", "bread", "wine", "parmesan", "peppers"]
        low_synergy = ["fish", "rice", "cream", "mushrooms"]
        
        if ingredient in high_synergy:
            return 0.9
        elif ingredient in medium_synergy:
            return 0.7
        elif ingredient in low_synergy:
            return 0.4
        else:
            return 0.5  # Default moderate synergy
    
    def create_tomato_love_declaration(self, intensity: int = 8) -> str:
        """Create a passionate declaration of tomato love."""
        declarations = {
            5: "I have a deep appreciation for the noble tomato.",
            6: "My heart holds a special place for the beautiful tomato.",
            7: "I am deeply, madly in love with tomatoes in all their forms!",
            8: "Tomatoes are my culinary soulmates, my kitchen companions, my edible poetry!",
            9: "I am utterly, completely, passionately OBSESSED with the divine tomato!",
            10: "TOMATOES ARE LIFE! TOMATOES ARE LOVE! TOMATOES ARE THE MEANING OF EXISTENCE!"
        }
        
        # Get appropriate declaration for intensity level
        for level in range(intensity, 4, -1):  # Work backwards to find appropriate level
            if level in declarations:
                return declarations[level]
        
        return declarations[5]  # Default fallback
    
    def suggest_seasonal_tomato_approach(self, season: str) -> str:
        """Suggest seasonal approach to tomato integration."""
        seasonal_approaches = {
            "spring": "In spring, my heart yearns for the promise of tomatoes to come. Let's use greenhouse gems or quality canned tomatoes to bridge the gap until summer's bounty arrives!",
            "summer": "SUMMER! The glorious season of tomato abundance! Fresh, ripe, sun-warmed tomatoes are at their peak - this is when tomato dreams come true!",
            "fall": "Autumn tomatoes carry the wisdom of the full growing season. Though fewer in number, they're deeply flavorful and perfect for preserving summer's memory.",
            "winter": "In winter's embrace, we turn to preserved tomatoes - canned, dried, or frozen - each one a captured ray of summer sunshine waiting to warm our souls."
        }
        
        return seasonal_approaches.get(season.lower(), seasonal_approaches["summer"])
    
    def evaluate_tomato_integration_success(self, content: str, obsession_level: int) -> float:
        """Evaluate how well tomatoes were integrated into content."""
        score = 0.0
        
        # Handle None or empty content
        if not content:
            return 0.0
            
        content_lower = content.lower()
        
        # Direct tomato mentions (50% of score)
        if "tomato" in content_lower:
            score += 0.5
            
            # Bonus for variety mentions
            varieties_mentioned = sum(1 for variety in TomatoVariety if variety.value in content_lower)
            score += min(0.2, varieties_mentioned * 0.05)
        
        # Tomato-related vocabulary (25% of score)
        tomato_related_words = ["ruby", "red", "vine", "garden", "sun-kissed", "juicy", "ripe", "fresh"]
        related_count = sum(1 for word in tomato_related_words if word in content_lower)
        score += min(0.25, related_count * 0.05)
        
        # Obsession-appropriate language (25% of score)
        obsession_words = ["love", "passion", "obsess", "adore", "worship", "divine", "magnificent"]
        obsession_count = sum(1 for word in obsession_words if word in content_lower)
        
        # Scale obsession language requirement by obsession level
        expected_obsession = obsession_level / 10.0
        actual_obsession = min(0.25, obsession_count * 0.05)
        
        # Score based on how well actual matches expected
        if expected_obsession > 0:
            obsession_score = min(0.25, actual_obsession / expected_obsession * 0.25)
        else:
            obsession_score = 0.25 if actual_obsession == 0 else actual_obsession
        
        score += obsession_score
        
        return min(1.0, score)