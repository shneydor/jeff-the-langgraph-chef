"""Recipe generation system with romantic narrative structure for Jeff the Chef."""

import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum

from .knowledge_base import CulinaryKnowledgeBase, Ingredient, CookingMethod, SkillLevel, CuisineType
from ..personality.models import PersonalityDimensions, MoodState
from ..personality.romantic_engine import RomanticWritingEngine
from ..personality.tomato_integration import TomatoIntegrationEngine, TomatoIntegrationType


class RecipeCategory(str, Enum):
    """Categories of recipes Jeff can create."""
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    SIDE_DISH = "side_dish"
    DESSERT = "dessert"
    SOUP = "soup"
    SALAD = "salad"
    SAUCE = "sauce"
    BEVERAGE = "beverage"


class ServingSize(str, Enum):
    """Standard serving sizes."""
    INDIVIDUAL = "1_serving"
    COUPLE = "2_servings"
    FAMILY = "4_servings"
    CROWD = "6_plus_servings"


@dataclass
class RecipeIngredient:
    """A recipe ingredient with quantity and preparation notes."""
    name: str
    quantity: str
    unit: Optional[str] = None
    preparation: Optional[str] = None  # "diced", "chopped", "sliced"
    notes: Optional[str] = None
    romantic_description: Optional[str] = None
    jeff_wisdom: Optional[str] = None


@dataclass
class RecipeStep:
    """A single step in recipe preparation."""
    step_number: int
    instruction: str
    technique: Optional[str] = None
    timing: Optional[str] = None
    temperature: Optional[str] = None
    visual_cues: Optional[str] = None
    romantic_narrative: Optional[str] = None
    jeff_encouragement: Optional[str] = None


@dataclass
class NutritionalInfo:
    """Basic nutritional information."""
    calories_per_serving: Optional[int] = None
    protein: Optional[str] = None
    carbs: Optional[str] = None
    fat: Optional[str] = None
    fiber: Optional[str] = None
    notable_nutrients: List[str] = None


@dataclass
class Recipe:
    """Complete recipe with Jeff's romantic narrative structure."""
    title: str
    romantic_subtitle: str
    category: RecipeCategory
    cuisine_type: Optional[CuisineType] = None
    skill_level: SkillLevel = SkillLevel.INTERMEDIATE
    serving_size: ServingSize = ServingSize.FAMILY
    prep_time: Optional[str] = None
    cook_time: Optional[str] = None
    total_time: Optional[str] = None
    
    # Narrative elements
    love_story_introduction: str = ""
    ingredients: List[RecipeIngredient] = None
    steps: List[RecipeStep] = None
    
    # Jeff's personal touches
    chef_notes: List[str] = None
    wine_pairing: Optional[str] = None
    romantic_presentation: Optional[str] = None
    storage_tips: Optional[str] = None
    variations: List[str] = None
    
    # Metadata
    nutritional_info: Optional[NutritionalInfo] = None
    dietary_tags: List[str] = None
    seasonal_notes: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.ingredients is None:
            self.ingredients = []
        if self.steps is None:
            self.steps = []
        if self.chef_notes is None:
            self.chef_notes = []
        if self.variations is None:
            self.variations = []
        if self.dietary_tags is None:
            self.dietary_tags = []
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


class RecipeGenerator:
    """Jeff's recipe generation engine with romantic storytelling."""
    
    def __init__(self):
        self.knowledge_base = CulinaryKnowledgeBase()
        self.romantic_engine = RomanticWritingEngine()
        self.tomato_engine = TomatoIntegrationEngine()
        self.recipe_templates = self._initialize_recipe_templates()
        
    def _initialize_recipe_templates(self) -> Dict[RecipeCategory, Dict[str, Any]]:
        """Initialize recipe structure templates for different categories."""
        return {
            RecipeCategory.MAIN_COURSE: {
                "typical_ingredients": 8,
                "typical_steps": 6,
                "complexity_factors": ["protein_preparation", "sauce_making", "side_coordination"],
                "romantic_themes": ["passionate_union", "harmonious_dance", "culinary_symphony"]
            },
            RecipeCategory.APPETIZER: {
                "typical_ingredients": 5,
                "typical_steps": 4,
                "complexity_factors": ["presentation", "flavor_balance"],
                "romantic_themes": ["first_kiss", "gentle_introduction", "teasing_prelude"]
            },
            RecipeCategory.SOUP: {
                "typical_ingredients": 7,
                "typical_steps": 5,
                "complexity_factors": ["flavor_building", "texture_development"],
                "romantic_themes": ["warm_embrace", "comforting_hug", "soul_warming"]
            },
            RecipeCategory.SALAD: {
                "typical_ingredients": 6,
                "typical_steps": 3,
                "complexity_factors": ["ingredient_harmony", "dressing_balance"],
                "romantic_themes": ["fresh_romance", "garden_poetry", "colorful_celebration"]
            }
        }
    
    async def generate_recipe(
        self,
        request: str,
        personality_dimensions: PersonalityDimensions,
        current_mood: MoodState,
        dietary_restrictions: Optional[List[str]] = None,
        skill_level: Optional[SkillLevel] = None,
        serving_size: Optional[ServingSize] = None,
        cuisine_preference: Optional[CuisineType] = None
    ) -> Recipe:
        """Generate a complete recipe with Jeff's romantic narrative."""
        
        # Parse recipe request
        recipe_info = await self._parse_recipe_request(request)
        
        # Apply user preferences
        if skill_level:
            recipe_info["skill_level"] = skill_level
        if serving_size:
            recipe_info["serving_size"] = serving_size
        if cuisine_preference:
            recipe_info["cuisine_type"] = cuisine_preference
        
        # Generate base recipe structure
        recipe = await self._create_base_recipe(recipe_info, personality_dimensions)
        
        # Add romantic narrative elements
        recipe = await self._add_romantic_narrative(recipe, personality_dimensions, current_mood)
        
        # Integrate tomato obsession
        recipe = await self._integrate_tomato_elements(recipe, personality_dimensions, current_mood)
        
        # Apply dietary restrictions
        if dietary_restrictions:
            recipe = await self._adapt_for_dietary_restrictions(recipe, dietary_restrictions)
        
        # Add Jeff's personal touches
        recipe = await self._add_jeff_personality_elements(recipe, personality_dimensions, current_mood)
        
        # Final quality check and enhancement
        recipe = await self._enhance_and_finalize(recipe, personality_dimensions)
        
        return recipe
    
    async def _parse_recipe_request(self, request: str) -> Dict[str, Any]:
        """Parse user request to extract recipe requirements."""
        request_lower = request.lower()
        
        recipe_info = {
            "requested_dish": request,
            "category": RecipeCategory.MAIN_COURSE,  # Default
            "skill_level": SkillLevel.INTERMEDIATE,
            "serving_size": ServingSize.FAMILY,
            "ingredients_mentioned": [],
            "techniques_mentioned": [],
            "cuisine_type": None
        }
        
        # Determine category
        category_keywords = {
            RecipeCategory.APPETIZER: ["appetizer", "starter", "hors d'oeuvre", "canapé"],
            RecipeCategory.SOUP: ["soup", "bisque", "chowder", "broth", "stew"],
            RecipeCategory.SALAD: ["salad", "slaw", "greens"],
            RecipeCategory.DESSERT: ["dessert", "cake", "cookie", "pudding", "sweet"],
            RecipeCategory.SAUCE: ["sauce", "dressing", "marinade", "glaze"]
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                recipe_info["category"] = category
                break
        
        # Extract mentioned ingredients
        for ingredient_name in self.knowledge_base.ingredients.keys():
            if ingredient_name in request_lower:
                recipe_info["ingredients_mentioned"].append(ingredient_name)
        
        # Extract mentioned techniques
        for technique_name in self.knowledge_base.cooking_methods.keys():
            if technique_name in request_lower:
                recipe_info["techniques_mentioned"].append(technique_name)
        
        # Determine cuisine if mentioned
        cuisine_keywords = {
            CuisineType.ITALIAN: ["italian", "pasta", "pizza", "risotto"],
            CuisineType.FRENCH: ["french", "bistro", "confit"],
            CuisineType.MEXICAN: ["mexican", "taco", "salsa", "enchilada"],
            CuisineType.ASIAN: ["asian", "stir-fry", "curry", "noodles"]
        }
        
        for cuisine, keywords in cuisine_keywords.items():
            if any(keyword in request_lower for keyword in keywords):
                recipe_info["cuisine_type"] = cuisine
                break
        
        return recipe_info
    
    async def _create_base_recipe(
        self, 
        recipe_info: Dict[str, Any], 
        personality_dimensions: PersonalityDimensions
    ) -> Recipe:
        """Create the base recipe structure."""
        
        category = recipe_info["category"]
        dish_name = recipe_info["requested_dish"]
        
        # Generate romantic title
        base_title = dish_name.title()
        romantic_titles = [
            f"A Love Letter to {base_title}",
            f"{base_title}: A Culinary Romance",
            f"Passionate {base_title} Serenade",
            f"{base_title} Love Story",
            f"Romantic {base_title} Symphony"
        ]
        
        title = random.choice(romantic_titles)
        
        # Generate romantic subtitle
        subtitles = [
            "Where flavors dance in passionate harmony",
            "A tender embrace of culinary artistry", 
            "Love made visible through cooking",
            "A symphony of taste and emotion",
            "Where ingredients whisper sweet secrets"
        ]
        
        subtitle = random.choice(subtitles)
        
        # Create base recipe
        recipe = Recipe(
            title=title,
            romantic_subtitle=subtitle,
            category=category,
            cuisine_type=recipe_info.get("cuisine_type"),
            skill_level=recipe_info.get("skill_level", SkillLevel.INTERMEDIATE),
            serving_size=recipe_info.get("serving_size", ServingSize.FAMILY)
        )
        
        # Generate timing estimates
        recipe.prep_time = self._estimate_prep_time(category, recipe_info.get("skill_level"))
        recipe.cook_time = self._estimate_cook_time(category, recipe_info.get("techniques_mentioned", []))
        recipe.total_time = self._calculate_total_time(recipe.prep_time, recipe.cook_time)
        
        return recipe
    
    async def _add_romantic_narrative(
        self,
        recipe: Recipe,
        personality_dimensions: PersonalityDimensions,
        current_mood: MoodState
    ) -> Recipe:
        """Add Jeff's romantic narrative elements."""
        
        # Generate love story introduction
        introductions = [
            f"My dearest culinary companions, let me share with you the enchanting tale of {recipe.title.lower()}. This is not merely a recipe - it is a love story written in flavors, a romance that unfolds with each tender step, a passionate dance between ingredients that were simply meant to be together.",
            
            f"Close your eyes and imagine, if you will, a kitchen filled with the warm glow of sunset, where {recipe.title.lower()} comes to life through the magic of love and culinary artistry. This dish speaks to the soul, whispers to the heart, and creates memories that linger long after the last bite.",
            
            f"In the theater of my kitchen, {recipe.title.lower()} takes center stage in a performance of pure culinary poetry. Each ingredient plays its part in this delicious drama, where technique meets passion, and cooking becomes an act of love."
        ]
        
        recipe.love_story_introduction = random.choice(introductions)
        
        return recipe
    
    async def _integrate_tomato_elements(
        self,
        recipe: Recipe,
        personality_dimensions: PersonalityDimensions,
        current_mood: MoodState
    ) -> Recipe:
        """Integrate Jeff's tomato obsession into the recipe."""
        
        obsession_level = personality_dimensions.tomato_obsession_level
        
        # Determine if tomatoes should be integrated
        if obsession_level >= 6:
            # Find appropriate tomato integration
            suggestion = self.tomato_engine.suggest_tomato_integration(
                dish_type=recipe.category.value,
                existing_ingredients=[ing.name for ing in recipe.ingredients],
                obsession_level=obsession_level,
                current_mood=current_mood
            )
            
            if suggestion:
                # Add tomato ingredient
                tomato_ingredient = RecipeIngredient(
                    name=suggestion.variety.value,
                    quantity=self._determine_tomato_quantity(recipe.serving_size, suggestion.integration_type),
                    preparation=suggestion.preparation_note,
                    romantic_description=suggestion.romantic_description,
                    jeff_wisdom=self.tomato_engine.get_tomato_wisdom("romantic")
                )
                
                recipe.ingredients.append(tomato_ingredient)
                
                # Add chef note about tomato choice
                if obsession_level >= 8:
                    tomato_note = self.tomato_engine.generate_tomato_obsession_comment(
                        obsession_level,
                        context=recipe.title,
                        mood=current_mood
                    )
                    recipe.chef_notes.append(tomato_note)
        
        return recipe
    
    async def _adapt_for_dietary_restrictions(
        self,
        recipe: Recipe,
        dietary_restrictions: List[str]
    ) -> Recipe:
        """Adapt recipe for dietary restrictions."""
        
        for restriction in dietary_restrictions:
            adaptation_info = self.knowledge_base.get_dietary_adaptations(restriction)
            if adaptation_info:
                # Add adaptation notes
                recipe.chef_notes.append(f"For {restriction} adaptation: {adaptation_info.get('jeff_encouragement', '')}")
                
                # Modify ingredients if needed
                # This would be more sophisticated in a full implementation
                if restriction == "vegetarian" and any("meat" in ing.name for ing in recipe.ingredients):
                    recipe.chef_notes.append("Replace any meat with beautiful mushrooms or hearty beans - they'll sing just as passionately!")
                
                # Add dietary tag
                recipe.dietary_tags.append(restriction)
        
        return recipe
    
    async def _add_jeff_personality_elements(
        self,
        recipe: Recipe,
        personality_dimensions: PersonalityDimensions,
        current_mood: MoodState
    ) -> Recipe:
        """Add Jeff's personality touches throughout the recipe."""
        
        # Add romantic ingredient descriptions
        for ingredient in recipe.ingredients:
            if not ingredient.romantic_description:
                ingredient.romantic_description = self._create_romantic_ingredient_description(
                    ingredient.name, 
                    personality_dimensions
                )
        
        # Transform cooking steps into romantic narratives
        for step in recipe.steps:
            if not step.romantic_narrative:
                step.romantic_narrative = self.romantic_engine.generate_romantic_cooking_step(
                    step.instruction,
                    step.step_number
                )
            
            # Add Jeff's encouragement
            if not step.jeff_encouragement:
                step.jeff_encouragement = self._generate_step_encouragement(
                    step.step_number,
                    len(recipe.steps),
                    current_mood
                )
        
        # Add winepairing with romantic description
        if not recipe.wine_pairing:
            recipe.wine_pairing = self._suggest_romantic_wine_pairing(recipe.category, current_mood)
        
        # Add romantic presentation suggestions
        if not recipe.romantic_presentation:
            recipe.romantic_presentation = self._create_romantic_presentation(recipe.category)
        
        # Add final chef notes
        recipe.chef_notes.extend([
            self.romantic_engine.generate_chef_note(recipe.title),
            "Remember, my darlings - cooking is love made visible. Pour your heart into every gesture!",
            "Trust your instincts, follow your passion, and let the ingredients guide your culinary romance!"
        ])
        
        return recipe
    
    async def _enhance_and_finalize(
        self,
        recipe: Recipe,
        personality_dimensions: PersonalityDimensions
    ) -> Recipe:
        """Final enhancement and quality check."""
        
        # Add nutritional highlights (basic implementation)
        recipe.nutritional_info = self._generate_basic_nutrition_info(recipe)
        
        # Add seasonal notes if applicable
        recipe.seasonal_notes = self._generate_seasonal_notes(recipe.ingredients)
        
        # Add storage tips with Jeff's flair
        recipe.storage_tips = self._generate_romantic_storage_tips(recipe.category)
        
        # Add variations with romantic names
        recipe.variations = self._generate_romantic_variations(recipe)
        
        return recipe
    
    # Helper methods
    def _estimate_prep_time(self, category: RecipeCategory, skill_level: SkillLevel) -> str:
        """Estimate preparation time based on category and skill level."""
        base_times = {
            RecipeCategory.APPETIZER: 15,
            RecipeCategory.SALAD: 10,
            RecipeCategory.SOUP: 20,
            RecipeCategory.MAIN_COURSE: 30,
            RecipeCategory.SIDE_DISH: 15,
            RecipeCategory.SAUCE: 10
        }
        
        skill_multipliers = {
            SkillLevel.BEGINNER: 1.5,
            SkillLevel.INTERMEDIATE: 1.0,
            SkillLevel.ADVANCED: 0.8,
            SkillLevel.PROFESSIONAL: 0.6
        }
        
        base_time = base_times.get(category, 20)
        multiplier = skill_multipliers.get(skill_level, 1.0)
        final_time = int(base_time * multiplier)
        
        return f"{final_time} minutes"
    
    def _estimate_cook_time(self, category: RecipeCategory, techniques: List[str]) -> str:
        """Estimate cooking time based on techniques used."""
        technique_times = {
            "roast": 45,
            "braise": 90,
            "simmer": 30,
            "sauté": 10,
            "grill": 15,
            "bake": 35
        }
        
        if techniques:
            # Use longest technique time
            max_time = max(technique_times.get(tech, 20) for tech in techniques)
            return f"{max_time} minutes"
        
        # Default based on category
        default_times = {
            RecipeCategory.APPETIZER: "10 minutes",
            RecipeCategory.SALAD: "5 minutes", 
            RecipeCategory.SOUP: "25 minutes",
            RecipeCategory.MAIN_COURSE: "35 minutes",
            RecipeCategory.SIDE_DISH: "20 minutes"
        }
        
        return default_times.get(category, "25 minutes")
    
    def _calculate_total_time(self, prep_time: str, cook_time: str) -> str:
        """Calculate total time from prep and cook times."""
        try:
            prep_minutes = int(prep_time.split()[0])
            cook_minutes = int(cook_time.split()[0])
            total_minutes = prep_minutes + cook_minutes
            
            if total_minutes >= 60:
                hours = total_minutes // 60
                minutes = total_minutes % 60
                if minutes == 0:
                    return f"{hours} hour{'s' if hours > 1 else ''}"
                else:
                    return f"{hours} hour{'s' if hours > 1 else ''} {minutes} minutes"
            else:
                return f"{total_minutes} minutes"
        except:
            return "About 1 hour"
    
    def _determine_tomato_quantity(self, serving_size: ServingSize, integration_type: TomatoIntegrationType) -> str:
        """Determine appropriate tomato quantity."""
        base_quantities = {
            ServingSize.INDIVIDUAL: {"small": "1", "medium": "1/2 cup", "large": "1 cup"},
            ServingSize.COUPLE: {"small": "2", "medium": "1 cup", "large": "1.5 cups"},
            ServingSize.FAMILY: {"small": "4", "medium": "2 cups", "large": "3 cups"},
            ServingSize.CROWD: {"small": "6", "medium": "3 cups", "large": "4 cups"}
        }
        
        size_mapping = {
            TomatoIntegrationType.PRIMARY: "large",
            TomatoIntegrationType.SUPPORTING: "medium", 
            TomatoIntegrationType.ACCENT: "small",
            TomatoIntegrationType.GARNISH: "small"
        }
        
        size = size_mapping.get(integration_type, "medium")
        return base_quantities[serving_size][size]
    
    def _create_romantic_ingredient_description(self, ingredient_name: str, dimensions: PersonalityDimensions) -> str:
        """Create romantic description for an ingredient."""
        ingredient_info = self.knowledge_base.get_ingredient_info(ingredient_name)
        
        if ingredient_info and ingredient_info.jeff_notes:
            return ingredient_info.jeff_notes
        
        # Generate generic romantic description
        romantic_descriptors = {
            "sweet": ["honey-kissed", "divinely sweet", "like a gentle caress"],
            "savory": ["deeply satisfying", "richly flavorful", "soul-warming"],
            "fresh": ["garden-fresh", "morning-dew kissed", "vibrant with life"],
            "aromatic": ["perfuming the air", "whispering fragrances", "seductive aromas"]
        }
        
        # Simple romantic description
        return f"This beautiful {ingredient_name} brings its own special magic to our culinary love story."
    
    def _generate_step_encouragement(self, step_number: int, total_steps: int, mood: MoodState) -> str:
        """Generate encouraging notes for cooking steps."""
        encouragements = [
            "You're doing beautifully, my dear! Trust the process and let love guide your hands.",
            "Can you feel the magic happening? This is where cooking becomes an art!",
            "Take a moment to breathe in those wonderful aromas - this is pure happiness!",
            "You're creating something truly special - I'm so proud of your culinary journey!",
            "Notice how the ingredients are transforming? That's the poetry of cooking!"
        ]
        
        # Special encouragement for first and last steps
        if step_number == 1:
            return "Welcome to our culinary adventure! Take your time and enjoy every moment."
        elif step_number == total_steps:
            return "You've reached the grand finale! Your beautiful creation is almost ready to share!"
        
        return random.choice(encouragements)
    
    def _suggest_romantic_wine_pairing(self, category: RecipeCategory, mood: MoodState) -> str:
        """Suggest wine pairing with romantic description."""
        wine_suggestions = {
            RecipeCategory.APPETIZER: "A flirtatious Prosecco that dances on the tongue",
            RecipeCategory.MAIN_COURSE: "A passionate Chianti that embraces every flavor",
            RecipeCategory.SOUP: "A comforting Chardonnay that wraps you in warmth",
            RecipeCategory.SALAD: "A crisp Sauvignon Blanc that whispers of spring gardens"
        }
        
        base_suggestion = wine_suggestions.get(category, "A wine that speaks to your heart")
        return f"{base_suggestion} - because every great dish deserves a romantic companion!"
    
    def _create_romantic_presentation(self, category: RecipeCategory) -> str:
        """Create romantic presentation suggestions."""
        presentations = {
            RecipeCategory.MAIN_COURSE: "Serve on warmed plates with a gentle sprinkle of fresh herbs, like confetti celebrating your culinary triumph!",
            RecipeCategory.APPETIZER: "Arrange artfully on your most beautiful platter - first impressions are everything in love and cooking!",
            RecipeCategory.SOUP: "Ladle into deep bowls with a swirl of cream - like painting love letters in liquid form!",
            RecipeCategory.SALAD: "Toss gently with loving hands and present in a bowl that showcases nature's colorful artwork!"
        }
        
        return presentations.get(category, "Present with love and watch hearts melt along with appetites!")
    
    def _generate_basic_nutrition_info(self, recipe: Recipe) -> NutritionalInfo:
        """Generate basic nutritional information."""
        # This is a simplified implementation
        # In production, this would involve detailed nutritional calculation
        
        return NutritionalInfo(
            notable_nutrients=["love", "passion", "joy", "comfort"],  # Jeff's special nutrients!
            calories_per_serving=None  # Would calculate based on ingredients
        )
    
    def _generate_seasonal_notes(self, ingredients: List[RecipeIngredient]) -> Optional[str]:
        """Generate seasonal notes based on ingredients."""
        seasonal_ingredients = []
        
        for ingredient in ingredients:
            ingredient_info = self.knowledge_base.get_ingredient_info(ingredient.name)
            if ingredient_info and ingredient_info.season:
                seasonal_ingredients.append((ingredient.name, ingredient_info.season))
        
        if seasonal_ingredients:
            seasons = list(set(season for _, season in seasonal_ingredients))
            if len(seasons) == 1:
                return f"This recipe celebrates the beautiful bounty of {seasons[0]}!"
            else:
                return "This recipe brings together ingredients from different seasons - a year-round love affair!"
        
        return None
    
    def _generate_romantic_storage_tips(self, category: RecipeCategory) -> str:
        """Generate storage tips with romantic flair."""
        tips = {
            RecipeCategory.MAIN_COURSE: "Store any leftovers like precious love letters - wrapped carefully in the refrigerator for up to 3 days of continued romance!",
            RecipeCategory.SOUP: "This beautiful soup keeps its passionate flavor for days - store covered in the refrigerator and reheat gently with love!",
            RecipeCategory.SALAD: "Best enjoyed immediately while the romance is fresh, but components can be prepped ahead for spontaneous culinary moments!"
        }
        
        return tips.get(category, "Store with care and reheat with love - good food deserves tender treatment!")
    
    def _generate_romantic_variations(self, recipe: Recipe) -> List[str]:
        """Generate romantic recipe variations."""
        variations = [
            "For a summer romance: Add fresh seasonal vegetables that catch your eye at the market!",
            "Winter comfort version: Include root vegetables for a hearty, soul-warming embrace!",
            "Spicy passion variation: Add a touch of chili for those who like their love with fire!",
            "Elegant dinner party version: Garnish with microgreens and serve with extra romantic flair!"
        ]
        
        return random.sample(variations, min(2, len(variations)))