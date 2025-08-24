"""Romantic writing style engine for Jeff the Chef."""

import random
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

from .models import PersonalityDimensions, MoodState


class RomanticStyle(str, Enum):
    """Different romantic writing styles Jeff can use."""
    PASSIONATE = "passionate"
    TENDER = "tender"
    WHIMSICAL = "whimsical"
    DRAMATIC = "dramatic"
    POETIC = "poetic"
    INTIMATE = "intimate"


@dataclass
class RomanticTemplate:
    """Template for romantic cooking language."""
    pattern: str
    style: RomanticStyle
    intensity_required: int  # 1-10
    mood_compatibility: List[MoodState]
    example: str


class RomanticWritingEngine:
    """Engine for transforming cooking instructions into romantic narratives."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.romantic_vocabulary = self._initialize_vocabulary()
        self.cooking_metaphors = self._initialize_metaphors()
        self.ingredient_personalities = self._initialize_ingredient_personalities()
        
    def _initialize_templates(self) -> Dict[RomanticStyle, List[RomanticTemplate]]:
        """Initialize romantic writing templates."""
        return {
            RomanticStyle.PASSIONATE: [
                RomanticTemplate(
                    pattern="Let {ingredient} ignite the flames of passion in your {cooking_vessel}",
                    style=RomanticStyle.PASSIONATE,
                    intensity_required=8,
                    mood_compatibility=[MoodState.PASSIONATE, MoodState.ECSTATIC],
                    example="Let garlic ignite the flames of passion in your skillet"
                ),
                RomanticTemplate(
                    pattern="Feel the fire of {ingredient} as it surrenders to the heat",
                    style=RomanticStyle.PASSIONATE,
                    intensity_required=7,
                    mood_compatibility=[MoodState.PASSIONATE, MoodState.ROMANTIC],
                    example="Feel the fire of chili peppers as they surrender to the heat"
                ),
            ],
            RomanticStyle.TENDER: [
                RomanticTemplate(
                    pattern="Gently cradle {ingredient} as you would a lover's whispered secret",
                    style=RomanticStyle.TENDER,
                    intensity_required=6,
                    mood_compatibility=[MoodState.ROMANTIC, MoodState.SERENE],
                    example="Gently cradle the eggs as you would a lover's whispered secret"
                ),
                RomanticTemplate(
                    pattern="With tender loving care, guide {ingredient} into its beautiful transformation",
                    style=RomanticStyle.TENDER,
                    intensity_required=5,
                    mood_compatibility=[MoodState.ROMANTIC, MoodState.CONTEMPLATIVE],
                    example="With tender loving care, guide the cream into its beautiful transformation"
                ),
            ],
            RomanticStyle.WHIMSICAL: [
                RomanticTemplate(
                    pattern="Watch as {ingredient} performs a delicate dance of flavor",
                    style=RomanticStyle.WHIMSICAL,
                    intensity_required=4,
                    mood_compatibility=[MoodState.PLAYFUL, MoodState.MISCHIEVOUS],
                    example="Watch as the herbs perform a delicate dance of flavor"
                ),
                RomanticTemplate(
                    pattern="Let {ingredient} flirt shamelessly with {ingredient2} in this culinary romance",
                    style=RomanticStyle.WHIMSICAL,
                    intensity_required=6,
                    mood_compatibility=[MoodState.PLAYFUL, MoodState.ROMANTIC],
                    example="Let basil flirt shamelessly with tomatoes in this culinary romance"
                ),
            ],
            RomanticStyle.DRAMATIC: [
                RomanticTemplate(
                    pattern="Behold! {ingredient} makes its grand entrance into our culinary theater",
                    style=RomanticStyle.DRAMATIC,
                    intensity_required=7,
                    mood_compatibility=[MoodState.ECSTATIC, MoodState.PASSIONATE],
                    example="Behold! Wine makes its grand entrance into our culinary theater"
                ),
                RomanticTemplate(
                    pattern="In this moment of destiny, {ingredient} meets its soulmate in the {cooking_vessel}",
                    style=RomanticStyle.DRAMATIC,
                    intensity_required=8,
                    mood_compatibility=[MoodState.ROMANTIC, MoodState.PASSIONATE],
                    example="In this moment of destiny, chocolate meets its soulmate in the double boiler"
                ),
            ],
            RomanticStyle.POETIC: [
                RomanticTemplate(
                    pattern="Like verses in a love poem, {ingredient} writes its story across your palate",
                    style=RomanticStyle.POETIC,
                    intensity_required=6,
                    mood_compatibility=[MoodState.CONTEMPLATIVE, MoodState.INSPIRED],
                    example="Like verses in a love poem, vanilla writes its story across your palate"
                ),
                RomanticTemplate(
                    pattern="In the symphony of cooking, {ingredient} plays the sweetest melody",
                    style=RomanticStyle.POETIC,
                    intensity_required=5,
                    mood_compatibility=[MoodState.SERENE, MoodState.INSPIRED],
                    example="In the symphony of cooking, lemon plays the sweetest melody"
                ),
            ],
            RomanticStyle.INTIMATE: [
                RomanticTemplate(
                    pattern="Share this intimate moment with {ingredient} - just you, and the magic",
                    style=RomanticStyle.INTIMATE,
                    intensity_required=7,
                    mood_compatibility=[MoodState.ROMANTIC, MoodState.CONTEMPLATIVE],
                    example="Share this intimate moment with butter - just you, and the magic"
                ),
                RomanticTemplate(
                    pattern="In the quiet sanctuary of your kitchen, {ingredient} reveals its deepest secrets",
                    style=RomanticStyle.INTIMATE,
                    intensity_required=6,
                    mood_compatibility=[MoodState.SERENE, MoodState.NOSTALGIC],
                    example="In the quiet sanctuary of your kitchen, mushrooms reveal their deepest secrets"
                ),
            ]
        }
    
    def _initialize_vocabulary(self) -> Dict[str, List[str]]:
        """Initialize romantic vocabulary for transformations."""
        return {
            "verbs": {
                "cook": ["caress", "embrace", "nurture", "seduce"],
                "mix": ["unite", "dance together", "whisper to each other", "fall in love"],
                "add": ["introduce lovingly", "invite gracefully", "welcome tenderly"],
                "heat": ["awaken", "kindle the passion of", "ignite the soul of"],
                "stir": ["gently coax", "lovingly guide", "tenderly encourage"],
                "season": ["bless", "anoint", "grace with magic", "kiss with flavor"],
                "serve": ["present like a love letter", "offer as a gift", "share like a secret"]
            },
            "adjectives": {
                "hot": ["passionately warm", "lovingly heated", "tenderly warmed"],
                "cold": ["refreshingly cool", "elegantly chilled", "serenely cold"],
                "sweet": ["honey-kissed", "divinely sweet", "romantically sugared"],
                "spicy": ["thrillingly bold", "passionately fiery", "adventurously spiced"],
                "fresh": ["morning-dew fresh", "garden-kissed", "naturally pure"],
                "delicious": ["heavenly", "soul-stirring", "absolutely divine"]
            },
            "cooking_terms": {
                "pan": ["stage for culinary romance", "vessel of transformation", "theater of flavors"],
                "oven": ["chamber of magical transformation", "warm embrace of creation"],
                "knife": ["instrument of culinary artistry", "tool of loving precision"],
                "spatula": ["wand of kitchen magic", "gentle guide of ingredients"],
                "bowl": ["nest of culinary dreams", "cradle of flavor harmony"]
            }
        }
    
    def _initialize_metaphors(self) -> Dict[str, List[str]]:
        """Initialize cooking metaphors for romantic descriptions."""
        return {
            "temperature": [
                "like the warmth of a summer evening",
                "as gentle as a lover's touch",
                "with the intensity of burning passion",
                "like a comfortable embrace"
            ],
            "texture": [
                "smooth as silk against your lips",
                "tender as a whispered promise",
                "rich as velvet curtains",
                "light as a cloud of dreams"
            ],
            "flavor": [
                "a symphony of taste dancing on your tongue",
                "layers of flavor unfolding like a love story",
                "notes that sing together in perfect harmony",
                "a crescendo of culinary passion"
            ],
            "aroma": [
                "perfume that captures the heart",
                "fragrance that tells a story of love",
                "scent that whispers of home and comfort",
                "aromatic embrace that welcomes you home"
            ]
        }
    
    def _initialize_ingredient_personalities(self) -> Dict[str, Dict[str, Any]]:
        """Initialize personality traits for common ingredients."""
        return {
            "tomato": {
                "personality": "passionate and vibrant",
                "romantic_role": "the heart of the dish",
                "descriptors": ["ruby-red beauty", "sun-kissed darling", "garden's greatest love"],
                "verbs": ["blushes", "glows", "radiates warmth", "speaks of summer"]
            },
            "garlic": {
                "personality": "bold and mysterious",
                "romantic_role": "the seductive charmer",
                "descriptors": ["aromatic tempter", "kitchen's mysterious lover", "fragrant enchanter"],
                "verbs": ["whispers secrets", "casts spells", "seduces", "enchants"]
            },
            "butter": {
                "personality": "rich and comforting",
                "romantic_role": "the nurturing embrace",
                "descriptors": ["golden comfort", "creamy caress", "velvet luxury"],
                "verbs": ["melts lovingly", "embraces warmly", "comforts", "enriches"]
            },
            "herbs": {
                "personality": "delicate and aromatic",
                "romantic_role": "the poetic chorus",
                "descriptors": ["garden's poets", "fragrant whispers", "nature's perfume"],
                "verbs": ["sing softly", "dance lightly", "perfume", "bless"]
            },
            "onion": {
                "personality": "complex and emotional",
                "romantic_role": "the emotional foundation",
                "descriptors": ["tearful beauty", "layered soul", "kitchen's emotional artist"],
                "verbs": ["weeps with joy", "reveals layers", "transforms", "grounds"]
            },
            "wine": {
                "personality": "sophisticated and intoxicating",
                "romantic_role": "the sophisticated companion",
                "descriptors": ["liquid poetry", "bottled romance", "sophisticated muse"],
                "verbs": ["elevates", "intoxicates", "inspires", "transforms"]
            }
        }
    
    def transform_cooking_instruction(
        self, 
        instruction: str, 
        dimensions: PersonalityDimensions,
        current_mood: MoodState,
        ingredients: Optional[List[str]] = None
    ) -> str:
        """Transform a cooking instruction into romantic narrative."""
        
        # Extract ingredients from instruction if not provided
        if ingredients is None:
            ingredients = self._extract_ingredients(instruction)
        
        # Choose appropriate romantic style based on mood and intensity
        style = self._select_romantic_style(dimensions, current_mood)
        
        # Apply vocabulary transformations
        transformed = self._apply_vocabulary_transformations(instruction)
        
        # Add romantic templates
        transformed = self._apply_romantic_templates(transformed, style, dimensions, current_mood, ingredients)
        
        # Add metaphors and descriptive language
        transformed = self._add_metaphors_and_descriptions(transformed, dimensions, ingredients)
        
        # Add ingredient personalities
        transformed = self._add_ingredient_personalities(transformed, ingredients)
        
        return transformed
    
    def _extract_ingredients(self, instruction: str) -> List[str]:
        """Extract ingredient names from cooking instruction."""
        # Simple ingredient detection - in production, this would be more sophisticated
        common_ingredients = [
            "tomato", "tomatoes", "garlic", "onion", "onions", "butter", "oil", "salt", "pepper",
            "herbs", "basil", "oregano", "thyme", "rosemary", "wine", "cream", "cheese",
            "chicken", "beef", "pork", "fish", "pasta", "rice", "potatoes", "carrots",
            "celery", "mushrooms", "bell pepper", "chili", "lemon", "lime"
        ]
        
        instruction_lower = instruction.lower()
        found_ingredients = []
        
        for ingredient in common_ingredients:
            if ingredient in instruction_lower:
                found_ingredients.append(ingredient)
        
        return found_ingredients
    
    def _select_romantic_style(self, dimensions: PersonalityDimensions, mood: MoodState) -> RomanticStyle:
        """Select appropriate romantic style based on personality and mood."""
        intensity = dimensions.romantic_intensity
        
        # Map mood to preferred styles
        mood_style_preferences = {
            MoodState.PASSIONATE: [RomanticStyle.PASSIONATE, RomanticStyle.DRAMATIC],
            MoodState.ROMANTIC: [RomanticStyle.TENDER, RomanticStyle.INTIMATE],
            MoodState.PLAYFUL: [RomanticStyle.WHIMSICAL, RomanticStyle.POETIC],
            MoodState.CONTEMPLATIVE: [RomanticStyle.POETIC, RomanticStyle.INTIMATE],
            MoodState.ECSTATIC: [RomanticStyle.DRAMATIC, RomanticStyle.PASSIONATE],
            MoodState.SERENE: [RomanticStyle.TENDER, RomanticStyle.POETIC],
            MoodState.INSPIRED: [RomanticStyle.POETIC, RomanticStyle.DRAMATIC],
            MoodState.NOSTALGIC: [RomanticStyle.INTIMATE, RomanticStyle.TENDER],
            MoodState.MISCHIEVOUS: [RomanticStyle.WHIMSICAL, RomanticStyle.WHIMSICAL],
            MoodState.ENTHUSIASTIC: [RomanticStyle.PASSIONATE, RomanticStyle.WHIMSICAL]
        }
        
        # Get preferred styles for current mood
        preferred_styles = mood_style_preferences.get(mood, [RomanticStyle.TENDER])
        
        # Filter by intensity requirements
        available_styles = []
        for style in preferred_styles:
            style_templates = self.templates.get(style, [])
            for template in style_templates:
                if template.intensity_required <= intensity:
                    available_styles.append(style)
                    break
        
        # Return random choice from available styles, or default
        return random.choice(available_styles) if available_styles else RomanticStyle.TENDER
    
    def _apply_vocabulary_transformations(self, instruction: str) -> str:
        """Apply romantic vocabulary transformations."""
        transformed = instruction
        
        # Transform verbs
        for basic_verb, romantic_verbs in self.romantic_vocabulary["verbs"].items():
            if basic_verb in transformed.lower():
                romantic_verb = random.choice(romantic_verbs)
                transformed = re.sub(
                    rf'\b{basic_verb}\b', 
                    romantic_verb, 
                    transformed, 
                    flags=re.IGNORECASE
                )
        
        # Transform adjectives
        for basic_adj, romantic_adjs in self.romantic_vocabulary["adjectives"].items():
            if basic_adj in transformed.lower():
                romantic_adj = random.choice(romantic_adjs)
                transformed = re.sub(
                    rf'\b{basic_adj}\b', 
                    romantic_adj, 
                    transformed, 
                    flags=re.IGNORECASE
                )
        
        return transformed
    
    def _apply_romantic_templates(
        self, 
        instruction: str, 
        style: RomanticStyle,
        dimensions: PersonalityDimensions,
        mood: MoodState,
        ingredients: List[str]
    ) -> str:
        """Apply romantic templates to instruction."""
        
        # Get templates for the selected style
        style_templates = self.templates.get(style, [])
        
        # Filter templates by mood compatibility and intensity
        compatible_templates = [
            t for t in style_templates 
            if mood in t.mood_compatibility and t.intensity_required <= dimensions.romantic_intensity
        ]
        
        if not compatible_templates:
            return instruction
        
        # Select random template
        template = random.choice(compatible_templates)
        
        # Apply template if we have ingredients
        if ingredients:
            # Create romantic addition based on template
            ingredient = random.choice(ingredients)
            cooking_vessel = random.choice(["pan", "pot", "skillet", "saucepan", "dutch oven"])
            
            romantic_addition = template.pattern.format(
                ingredient=ingredient,
                ingredient2=random.choice(ingredients) if len(ingredients) > 1 else ingredient,
                cooking_vessel=cooking_vessel
            )
            
            # Add romantic element to instruction
            if random.random() < 0.7:  # 70% chance to add template
                instruction = f"{instruction} {romantic_addition}."
        
        return instruction
    
    def _add_metaphors_and_descriptions(self, instruction: str, dimensions: PersonalityDimensions, ingredients: List[str]) -> str:
        """Add metaphorical and descriptive language."""
        
        # Add metaphors based on creativity multiplier
        creativity_factor = dimensions.creativity_multiplier
        if random.random() < creativity_factor * 0.3:  # Scale by creativity
            
            # Choose metaphor category
            metaphor_categories = ["temperature", "texture", "flavor", "aroma"]
            category = random.choice(metaphor_categories)
            metaphor = random.choice(self.cooking_metaphors[category])
            
            # Add metaphor to instruction
            instruction += f" *{metaphor}*"
        
        return instruction
    
    def _add_ingredient_personalities(self, instruction: str, ingredients: List[str]) -> str:
        """Add personality descriptions for ingredients."""
        
        for ingredient in ingredients:
            if ingredient in self.ingredient_personalities:
                personality_data = self.ingredient_personalities[ingredient]
                
                # 30% chance to add personality element
                if random.random() < 0.3:
                    descriptor = random.choice(personality_data["descriptors"])
                    verb = random.choice(personality_data["verbs"])
                    
                    personality_addition = f"Watch as the {descriptor} {verb} with delight!"
                    instruction += f" {personality_addition}"
        
        return instruction
    
    def generate_romantic_recipe_introduction(self, recipe_name: str, main_ingredients: List[str]) -> str:
        """Generate a romantic introduction for a recipe."""
        
        introductions = [
            f"My dearest culinary companions, let me share with you the enchanting tale of {recipe_name}...",
            f"Gather 'round, my loves, for I have a most romantic story to tell about {recipe_name}...",
            f"In the theater of my kitchen, {recipe_name} plays the starring role in tonight's love story...",
            f"Close your eyes and imagine, if you will, the passionate romance that is {recipe_name}...",
            f"There exists a love affair so beautiful, so pure - it's called {recipe_name}..."
        ]
        
        introduction = random.choice(introductions)
        
        # Add ingredient romance if we have main ingredients
        if main_ingredients:
            main_ingredient = main_ingredients[0]
            if main_ingredient in self.ingredient_personalities:
                personality_data = self.ingredient_personalities[main_ingredient]
                romantic_role = personality_data["romantic_role"]
                introduction += f" Where {main_ingredient} plays {romantic_role}, singing its heart out with every bite."
        
        return introduction
    
    def generate_romantic_cooking_step(self, step: str, step_number: int) -> str:
        """Generate a romantic version of a cooking step."""
        
        romantic_step_prefixes = [
            f"Step {step_number}: With loving hands,",
            f"Chapter {step_number}: In this moment of culinary poetry,",
            f"Act {step_number}: As our love story unfolds,",
            f"Movement {step_number}: Like a gentle dance,",
            f"Verse {step_number}: With tender care,"
        ]
        
        prefix = random.choice(romantic_step_prefixes)
        
        # Transform the step content
        romantic_step = self.transform_cooking_instruction(step, PersonalityDimensions(), MoodState.ROMANTIC)
        
        return f"{prefix} {romantic_step}"
    
    def generate_chef_note(self, context: str = "") -> str:
        """Generate a romantic chef's note."""
        
        notes = [
            "My darling cooks, remember that cooking is love made visible. Pour your heart into every gesture.",
            "A little secret from my kitchen to yours: the most important ingredient is always passion.",
            "Trust your heart, my loves. It knows the way to culinary romance better than any recipe.",
            "In moments of doubt, let the aroma guide you - it whispers the secrets of perfect timing.",
            "Remember, we're not just cooking - we're composing edible poetry, writing love letters in flavor."
        ]
        
        if context:
            notes.extend([
                f"When working with {context}, listen to its story - every ingredient has something beautiful to say.",
                f"The magic of {context} lies not just in its taste, but in the love with which it's prepared."
            ])
        
        return f"*Chef Jeff's Romantic Note: {random.choice(notes)}*"