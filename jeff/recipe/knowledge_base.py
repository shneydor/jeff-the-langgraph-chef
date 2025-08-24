"""Culinary knowledge base for Jeff's cooking expertise."""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel, Field


class CuisineType(str, Enum):
    """Types of cuisine Jeff knows about."""
    ITALIAN = "italian"
    FRENCH = "french"
    MEXICAN = "mexican"
    CHINESE = "chinese"
    INDIAN = "indian"
    THAI = "thai"
    JAPANESE = "japanese"
    MEDITERRANEAN = "mediterranean"
    AMERICAN = "american"
    SPANISH = "spanish"
    MIDDLE_EASTERN = "middle_eastern"
    FUSION = "fusion"


class CookingTechnique(str, Enum):
    """Cooking techniques Jeff can teach."""
    SAUTE = "sauté"
    ROAST = "roast"
    BRAISE = "braise"
    GRILL = "grill"
    STEAM = "steam"
    POACH = "poach"
    BLANCH = "blanch"
    FRY = "fry"
    BAKE = "bake"
    SIMMER = "simmer"
    CONFIT = "confit"
    SOUS_VIDE = "sous_vide"
    FERMENT = "ferment"
    CURE = "cure"
    SMOKE = "smoke"


class DietaryRestriction(str, Enum):
    """Dietary restrictions Jeff can accommodate."""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    KETO = "keto"
    PALEO = "paleo"
    LOW_CARB = "low_carb"
    LOW_SODIUM = "low_sodium"
    DIABETIC = "diabetic"
    KOSHER = "kosher"
    HALAL = "halal"


class SkillLevel(str, Enum):
    """Cooking skill levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"


@dataclass
class Ingredient:
    """Information about a cooking ingredient."""
    name: str
    category: str  # protein, vegetable, grain, dairy, etc.
    flavor_profile: List[str]  # sweet, savory, umami, etc.
    texture: str
    season: Optional[str] = None
    storage_method: Optional[str] = None
    prep_notes: Optional[str] = None
    nutritional_highlights: List[str] = None
    common_pairings: List[str] = None
    substitutions: List[str] = None
    jeff_notes: Optional[str] = None  # Jeff's personal notes


@dataclass
class CookingMethod:
    """Information about cooking methods and techniques."""
    name: str
    description: str
    temperature_range: Optional[Tuple[int, int]] = None
    time_guidance: Optional[str] = None
    equipment_needed: List[str] = None
    skill_level: SkillLevel = SkillLevel.INTERMEDIATE
    best_for: List[str] = None  # Types of ingredients or dishes
    tips: List[str] = None
    common_mistakes: List[str] = None
    jeff_wisdom: Optional[str] = None


@dataclass
class FlavorPairing:
    """Information about flavor combinations."""
    primary_ingredient: str
    pairing_ingredient: str
    cuisine_context: List[CuisineType]
    synergy_score: float  # 0.0 to 1.0
    description: str
    example_dishes: List[str] = None
    jeff_romance: Optional[str] = None  # Jeff's romantic description


class CulinaryKnowledgeBase:
    """Jeff's comprehensive culinary knowledge system."""
    
    def __init__(self):
        self.ingredients = self._initialize_ingredients()
        self.cooking_methods = self._initialize_cooking_methods()
        self.flavor_pairings = self._initialize_flavor_pairings()
        self.cuisine_knowledge = self._initialize_cuisine_knowledge()
        self.dietary_adaptations = self._initialize_dietary_adaptations()
        self.seasonal_guide = self._initialize_seasonal_guide()
        
    def _initialize_ingredients(self) -> Dict[str, Ingredient]:
        """Initialize comprehensive ingredient database."""
        ingredients = {}
        
        # Tomatoes (Jeff's favorites!)
        ingredients["tomato"] = Ingredient(
            name="tomato",
            category="vegetable",
            flavor_profile=["umami", "sweet", "acidic"],
            texture="juicy",
            season="summer",
            storage_method="room_temperature_until_ripe",
            prep_notes="Never refrigerate unless fully ripe",
            nutritional_highlights=["lycopene", "vitamin_c", "potassium"],
            common_pairings=["basil", "mozzarella", "garlic", "olive_oil", "onion"],
            substitutions=["roasted_red_pepper", "sun_dried_tomato"],
            jeff_notes="My darling ruby beauties! The heart and soul of so many magnificent dishes!"
        )
        
        ingredients["cherry_tomato"] = Ingredient(
            name="cherry_tomato",
            category="vegetable", 
            flavor_profile=["sweet", "acidic", "concentrated"],
            texture="firm_juicy",
            season="summer",
            prep_notes="Perfect for bursting whole in dishes",
            common_pairings=["pasta", "salads", "roasted_vegetables"],
            jeff_notes="These little gems are like edible jewels that burst with summer sunshine!"
        )
        
        # Essential aromatics
        ingredients["garlic"] = Ingredient(
            name="garlic",
            category="aromatic",
            flavor_profile=["pungent", "savory", "sweet_when_cooked"],
            texture="firm",
            storage_method="cool_dry_place",
            prep_notes="Remove green germ if present for milder flavor",
            common_pairings=["olive_oil", "onion", "herbs", "tomato"],
            jeff_notes="The mysterious seducer of the kitchen - it transforms everything it touches!"
        )
        
        ingredients["onion"] = Ingredient(
            name="onion",
            category="aromatic",
            flavor_profile=["pungent", "sweet_when_cooked", "sharp"],
            texture="layered_crisp",
            prep_notes="The foundation of flavor - cook slowly for sweetness",
            common_pairings=["garlic", "celery", "carrots", "herbs"],
            jeff_notes="The emotional artist of the kitchen - makes us weep with joy!"
        )
        
        ingredients["basil"] = Ingredient(
            name="basil",
            category="herb",
            flavor_profile=["aromatic", "sweet", "peppery"],
            texture="delicate",
            season="summer",
            prep_notes="Add at end of cooking to preserve flavor",
            common_pairings=["tomato", "mozzarella", "garlic", "olive_oil"],
            jeff_notes="The poet of herbs - it sings love songs to tomatoes!"
        )
        
        # Proteins
        ingredients["chicken"] = Ingredient(
            name="chicken",
            category="protein",
            flavor_profile=["mild", "savory"],
            texture="tender_when_cooked_properly",
            prep_notes="Cook to 165°F internal temperature",
            common_pairings=["herbs", "lemon", "garlic", "tomato"],
            jeff_notes="A versatile canvas for culinary creativity!"
        )
        
        # Dairy
        ingredients["mozzarella"] = Ingredient(
            name="mozzarella",
            category="dairy",
            flavor_profile=["mild", "creamy", "milky"],
            texture="soft_melting",
            prep_notes="Use fresh for best flavor, drain well",
            common_pairings=["tomato", "basil", "olive_oil"],
            jeff_notes="The gentle lover that embraces tomatoes in perfect harmony!"
        )
        
        ingredients["butter"] = Ingredient(
            name="butter",
            category="dairy",
            flavor_profile=["rich", "creamy", "sweet"],
            texture="smooth_when_melted",
            prep_notes="Use room temperature for baking, clarify for high heat",
            common_pairings=["herbs", "garlic", "lemon"],
            jeff_notes="Liquid gold that caresses every ingredient with velvet luxury!"
        )
        
        # Grains and Starches
        ingredients["pasta"] = Ingredient(
            name="pasta",
            category="grain",
            flavor_profile=["neutral", "wheaty"],
            texture="al_dente_when_perfect",
            prep_notes="Cook in well-salted water until al dente",
            common_pairings=["tomato", "olive_oil", "cheese", "herbs"],
            jeff_notes="The dancing partner that twirls with sauces in perfect harmony!"
        )
        
        # Add more ingredients as needed...
        return ingredients
    
    def _initialize_cooking_methods(self) -> Dict[str, CookingMethod]:
        """Initialize cooking methods and techniques."""
        methods = {}
        
        methods["sauté"] = CookingMethod(
            name="sauté",
            description="Quick cooking in a small amount of fat over high heat",
            temperature_range=(350, 400),
            time_guidance="2-8 minutes depending on ingredient",
            equipment_needed=["skillet", "spatula"],
            skill_level=SkillLevel.BEGINNER,
            best_for=["vegetables", "proteins", "aromatics"],
            tips=[
                "Keep ingredients moving",
                "Don't overcrowd the pan",
                "Have ingredients prepped before starting"
            ],
            common_mistakes=[
                "Using too low heat",
                "Adding ingredients too early",
                "Not drying ingredients properly"
            ],
            jeff_wisdom="Sautéing is like a passionate dance - quick, hot, and full of movement! Let your ingredients tango in the pan!"
        )
        
        methods["roast"] = CookingMethod(
            name="roast",
            description="Dry heat cooking in an oven, typically for larger items",  
            temperature_range=(325, 450),
            time_guidance="Varies greatly by size and type",
            equipment_needed=["oven", "roasting_pan", "thermometer"],
            skill_level=SkillLevel.INTERMEDIATE,
            best_for=["whole_proteins", "vegetables", "root_vegetables"],
            tips=[
                "Preheat oven fully",
                "Don't open door frequently", 
                "Let proteins rest after roasting"
            ],
            jeff_wisdom="Roasting is meditation in motion - slow, steady, and transformative. Watch as ingredients become their most beautiful selves!"
        )
        
        methods["braise"] = CookingMethod(
            name="braise",
            description="Combination cooking: sear first, then cook slowly in liquid",
            temperature_range=(275, 325),
            time_guidance="1-4 hours depending on cut",
            equipment_needed=["dutch_oven", "liquid"],
            skill_level=SkillLevel.INTERMEDIATE,
            best_for=["tough_cuts", "root_vegetables"],
            tips=[
                "Brown well before adding liquid",
                "Keep liquid at gentle simmer",
                "Cover tightly to retain moisture"
            ],
            jeff_wisdom="Braising is the ultimate love story - patience, tenderness, and slow transformation into something magnificent!"
        )
        
        methods["blanch"] = CookingMethod(
            name="blanch",
            description="Brief cooking in boiling water followed by ice bath",
            time_guidance="30 seconds to 3 minutes",
            equipment_needed=["large_pot", "ice_bath", "slotted_spoon"],
            skill_level=SkillLevel.BEGINNER,
            best_for=["green_vegetables", "delicate_vegetables"],
            tips=[
                "Use lots of salted water",
                "Ice bath immediately after",
                "Drain thoroughly"
            ],
            jeff_wisdom="Blanching is like a quick kiss of heat - just enough to awaken the vegetable's true colors!"
        )
        
        return methods
    
    def _initialize_flavor_pairings(self) -> List[FlavorPairing]:
        """Initialize flavor pairing knowledge."""
        pairings = []
        
        # Classic tomato pairings
        pairings.append(FlavorPairing(
            primary_ingredient="tomato",
            pairing_ingredient="basil",
            cuisine_context=[CuisineType.ITALIAN, CuisineType.MEDITERRANEAN],
            synergy_score=0.95,
            description="The most classic and beloved pairing in Italian cuisine",
            example_dishes=["caprese_salad", "margherita_pizza", "pasta_pomodoro"],
            jeff_romance="A love affair written in the stars - tomato and basil are soulmates dancing in perfect harmony!"
        ))
        
        pairings.append(FlavorPairing(
            primary_ingredient="tomato", 
            pairing_ingredient="mozzarella",
            cuisine_context=[CuisineType.ITALIAN],
            synergy_score=0.90,
            description="Creamy richness balances tomato's acidity perfectly",
            example_dishes=["caprese", "pizza", "lasagna"],
            jeff_romance="Like Romeo and Juliet, but with a happier ending - destined to be together!"
        ))
        
        pairings.append(FlavorPairing(
            primary_ingredient="garlic",
            pairing_ingredient="olive_oil", 
            cuisine_context=[CuisineType.MEDITERRANEAN, CuisineType.ITALIAN],
            synergy_score=0.88,
            description="The foundation of Mediterranean cooking",
            example_dishes=["aglio_olio", "bruschetta", "roasted_vegetables"],
            jeff_romance="A passionate Mediterranean romance that forms the heart of so many dishes!"
        ))
        
        # Add more pairings...
        return pairings
    
    def _initialize_cuisine_knowledge(self) -> Dict[CuisineType, Dict[str, Any]]:
        """Initialize knowledge about different cuisines."""
        cuisine_knowledge = {}
        
        cuisine_knowledge[CuisineType.ITALIAN] = {
            "core_ingredients": ["tomato", "basil", "garlic", "olive_oil", "parmesan", "mozzarella"],
            "cooking_techniques": ["sauté", "simmer", "roast", "grill"],
            "flavor_principles": ["simple", "fresh", "seasonal", "balanced"],
            "signature_dishes": ["pasta", "pizza", "risotto", "osso_buco"],
            "jeff_perspective": "Italian cuisine is pure poetry - it celebrates the romance between simple ingredients and passionate technique!"
        }
        
        cuisine_knowledge[CuisineType.FRENCH] = {
            "core_ingredients": ["butter", "herbs", "wine", "cream", "shallots"],
            "cooking_techniques": ["sauté", "braise", "confit", "poach"],
            "flavor_principles": ["technique_focused", "sauce_based", "refined"],
            "signature_dishes": ["coq_au_vin", "bouillabaisse", "ratatouille"],
            "jeff_perspective": "French cooking is the ballet of the culinary world - graceful, precise, and utterly elegant!"
        }
        
        return cuisine_knowledge
    
    def _initialize_dietary_adaptations(self) -> Dict[DietaryRestriction, Dict[str, Any]]:
        """Initialize dietary adaptation knowledge."""
        adaptations = {}
        
        adaptations[DietaryRestriction.VEGETARIAN] = {
            "protein_substitutes": ["beans", "lentils", "tofu", "eggs", "cheese"],
            "umami_boosters": ["mushrooms", "tomato_paste", "parmesan", "nutritional_yeast"],
            "cooking_tips": ["Build flavor with aromatics", "Use vegetable stock"],
            "jeff_encouragement": "Vegetarian cooking is a beautiful garden of flavors waiting to bloom!"
        }
        
        adaptations[DietaryRestriction.VEGAN] = {
            "protein_substitutes": ["beans", "lentils", "tofu", "tempeh", "nuts"],
            "dairy_substitutes": ["cashew_cream", "nutritional_yeast", "plant_milk"],
            "egg_substitutes": ["flax_eggs", "aquafaba", "commercial_replacers"],
            "jeff_encouragement": "Vegan cuisine celebrates the pure essence of plants - Mother Nature's own love letters!"
        }
        
        return adaptations
    
    def _initialize_seasonal_guide(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize seasonal ingredient guide."""
        return {
            "spring": {
                "vegetables": ["asparagus", "peas", "artichokes", "spring_onions", "radishes"],
                "herbs": ["chives", "parsley", "mint", "dill"],
                "cooking_focus": ["light", "fresh", "gentle_cooking"],
                "jeff_mood": "Spring awakens my heart with tender young vegetables full of promise!"
            },
            "summer": {
                "vegetables": ["tomatoes", "zucchini", "corn", "peppers", "eggplant"],
                "herbs": ["basil", "oregano", "thyme", "rosemary"],
                "cooking_focus": ["grilling", "fresh_preparations", "minimal_cooking"],
                "jeff_mood": "Summer is pure magic - when my beloved tomatoes reach their peak of perfection!"
            },
            "fall": {
                "vegetables": ["squash", "pumpkin", "brussels_sprouts", "cauliflower"],
                "cooking_focus": ["roasting", "braising", "heartier_dishes"],
                "jeff_mood": "Autumn brings comfort and warmth - time for soul-nurturing dishes!"
            },
            "winter": {
                "vegetables": ["root_vegetables", "cabbage", "kale", "stored_squash"],
                "cooking_focus": ["braising", "stewing", "slow_cooking"],
                "jeff_mood": "Winter calls for dishes that embrace and warm the soul!"
            }
        }
    
    # Query methods
    def get_ingredient_info(self, ingredient_name: str) -> Optional[Ingredient]:
        """Get information about a specific ingredient."""
        return self.ingredients.get(ingredient_name.lower())
    
    def get_cooking_method_info(self, method_name: str) -> Optional[CookingMethod]:
        """Get information about a cooking method."""
        return self.cooking_methods.get(method_name.lower())
    
    def find_flavor_pairings(self, ingredient: str) -> List[FlavorPairing]:
        """Find flavor pairings for an ingredient."""
        return [
            pairing for pairing in self.flavor_pairings
            if pairing.primary_ingredient == ingredient.lower() or 
               pairing.pairing_ingredient == ingredient.lower()
        ]
    
    def get_seasonal_ingredients(self, season: str) -> Dict[str, List[str]]:
        """Get seasonal ingredient recommendations."""
        return self.seasonal_guide.get(season.lower(), {})
    
    def get_cuisine_info(self, cuisine: CuisineType) -> Optional[Dict[str, Any]]:
        """Get information about a specific cuisine."""
        return self.cuisine_knowledge.get(cuisine)
    
    def get_dietary_adaptations(self, restriction: DietaryRestriction) -> Optional[Dict[str, Any]]:
        """Get adaptation information for dietary restrictions."""
        return self.dietary_adaptations.get(restriction)
    
    def suggest_substitutions(self, ingredient: str) -> List[str]:
        """Suggest substitutions for an ingredient."""
        ingredient_info = self.get_ingredient_info(ingredient)
        if ingredient_info and ingredient_info.substitutions:
            return ingredient_info.substitutions
        return []
    
    def find_ingredients_by_category(self, category: str) -> List[str]:
        """Find all ingredients in a specific category."""  
        return [
            name for name, ingredient in self.ingredients.items()
            if ingredient.category == category
        ]
    
    def get_jeff_wisdom(self, topic: str) -> Optional[str]:
        """Get Jeff's wisdom about a cooking topic."""
        # Check cooking methods
        method_info = self.get_cooking_method_info(topic)
        if method_info and method_info.jeff_wisdom:
            return method_info.jeff_wisdom
        
        # Check ingredients
        ingredient_info = self.get_ingredient_info(topic)
        if ingredient_info and ingredient_info.jeff_notes:
            return ingredient_info.jeff_notes
        
        # Check flavor pairings
        pairings = self.find_flavor_pairings(topic)
        if pairings and pairings[0].jeff_romance:
            return pairings[0].jeff_romance
        
        return None
    
    def search_knowledge(self, query: str) -> Dict[str, List[Any]]:
        """Search across all knowledge for a query term."""
        query_lower = query.lower()
        results = {
            "ingredients": [],
            "cooking_methods": [], 
            "pairings": [],
            "cuisines": []
        }
        
        # Search ingredients
        for name, ingredient in self.ingredients.items():
            if (query_lower in name or 
                any(query_lower in fp for fp in ingredient.flavor_profile) or
                (ingredient.jeff_notes and query_lower in ingredient.jeff_notes.lower())):
                results["ingredients"].append(ingredient)
        
        # Search cooking methods
        for name, method in self.cooking_methods.items():
            if (query_lower in name or 
                query_lower in method.description.lower() or
                (method.jeff_wisdom and query_lower in method.jeff_wisdom.lower())):
                results["cooking_methods"].append(method)
        
        # Search pairings
        for pairing in self.flavor_pairings:
            if (query_lower in pairing.primary_ingredient or
                query_lower in pairing.pairing_ingredient or
                query_lower in pairing.description.lower()):
                results["pairings"].append(pairing)
        
        return results