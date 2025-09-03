"""Input Processor Node for Jeff's LangGraph orchestration system."""

import re
from typing import Dict, List, Optional, Any, Tuple

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage, 
    ContentType,
    ProcessingPriority
)


class InputProcessorNode(BaseNode):
    """Processes and analyzes user input to extract intent and entities."""
    
    def __init__(self):
        super().__init__("input_processor")
        self.intent_patterns = self._initialize_intent_patterns()
    
    def _initialize_intent_patterns(self) -> Dict[ContentType, List[str]]:
        """Initialize patterns for intent recognition."""
        return {
            ContentType.RECIPE_REQUEST: [
                r"recipe for",
                r"how to make",
                r"how do i cook",
                r"show me.*recipe",
                r"i want to make",
                r"cooking.*recipe"
            ],
            ContentType.COOKING_QUESTION: [
                r"how to.*cook",
                r"what.*temperature",
                r"how long.*cook",
                r"cooking time",
                r"cooking method"
            ],
            ContentType.INGREDIENT_INQUIRY: [
                r"what is.*ingredient",
                r"substitute for",
                r"instead of",
                r"replace.*with",
                r"ingredient.*substitute"
            ],
            ContentType.TECHNIQUE_QUESTION: [
                r"how to.*technique",
                r"what.*method",
                r"cooking technique",
                r"how do you.*technique"
            ],
            ContentType.FOOD_PAIRING: [
                r"goes well with",
                r"pair.*with",
                r"what.*with",
                r"complement"
            ],
            ContentType.NUTRITION_QUESTION: [
                r"calories",
                r"nutrition",
                r"healthy",
                r"diet",
                r"nutritious"
            ],
            ContentType.IMAGE_REQUEST: [
                r"image of",
                r"picture of",
                r"photo of",
                r"show me.*image",
                r"create.*image",
                r"generate.*image",
                r"draw.*picture"
            ]
        }
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Process input to extract intent, entities, and context."""
        
        raw_input = state["raw_input"]
        
        # Extract intent
        content_type, confidence = self._classify_intent(raw_input)
        
        # Extract entities (ingredients, techniques, etc.)
        entities = await self._extract_entities(raw_input, content_type)
        
        # Determine processing priority
        priority = self._determine_priority(raw_input, content_type)
        
        # Update state
        state["content_type"] = content_type
        state["confidence_score"] = confidence
        state["extracted_entities"] = entities
        state["processing_priority"] = priority
        state["processed_input"] = raw_input.strip()
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.PERSONALITY_APPLIED)
        
        return state
    
    def _classify_intent(self, text: str) -> Tuple[ContentType, float]:
        """Classify user intent with confidence score."""
        text_lower = text.lower()
        intent_scores = {}
        
        for content_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            
            if score > 0:
                intent_scores[content_type] = score / len(patterns)
        
        if not intent_scores:
            return ContentType.GENERAL_CHAT, 0.3
        
        # Get highest scoring intent
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], min(best_intent[1], 1.0)
    
    async def _extract_entities(self, text: str, content_type: ContentType) -> Dict[str, Any]:
        """Extract entities like ingredients, techniques, cuisine types."""
        entities = {
            "ingredients": [],
            "techniques": [],
            "cuisine_types": [],
            "dietary_restrictions": [],
            "equipment": [],
            "measurements": [],
            "image_description": None,
            "image_style": None
        }
        
        # Simple pattern-based extraction (in production, would use NER)
        text_lower = text.lower()
        
        # Common ingredients
        common_ingredients = [
            "tomato", "tomatoes", "onion", "garlic", "chicken", "beef", "pork",
            "pasta", "rice", "potato", "carrot", "celery", "mushroom", "pepper",
            "salt", "oil", "butter", "cheese", "herbs", "spices"
        ]
        
        for ingredient in common_ingredients:
            if ingredient in text_lower:
                entities["ingredients"].append(ingredient)
        
        # Cooking techniques
        techniques = [
            "roast", "bake", "fry", "sauté", "grill", "steam", "boil",
            "simmer", "braise", "poach", "blanch", "marinate"
        ]
        
        for technique in techniques:
            if technique in text_lower:
                entities["techniques"].append(technique)
        
        # Cuisine types
        cuisines = [
            "italian", "french", "chinese", "mexican", "indian", "thai",
            "japanese", "mediterranean", "american", "spanish"
        ]
        
        for cuisine in cuisines:
            if cuisine in text_lower:
                entities["cuisine_types"].append(cuisine)
        
        # Dietary restrictions
        dietary = [
            "vegetarian", "vegan", "gluten-free", "dairy-free", "keto",
            "paleo", "low-carb", "low-fat", "sugar-free"
        ]
        
        for diet in dietary:
            if diet in text_lower:
                entities["dietary_restrictions"].append(diet)
        
        # Extract image-specific entities for image requests
        if content_type == ContentType.IMAGE_REQUEST:
            entities["image_description"] = self._extract_image_description(text)
            entities["image_style"] = self._extract_image_style(text)
        
        return entities
    
    def _extract_image_description(self, text: str) -> Optional[str]:
        """Extract image description from text."""
        # Remove image request keywords to get the actual description
        description = text.lower()
        
        # Remove common image request prefixes
        prefixes_to_remove = [
            "image of", "picture of", "photo of", "show me an image of",
            "create an image of", "generate an image of", "draw a picture of",
            "make an image of", "create a picture of"
        ]
        
        for prefix in prefixes_to_remove:
            if description.startswith(prefix):
                description = description[len(prefix):].strip()
                break
        
        return description if description else None
    
    def _extract_image_style(self, text: str) -> Optional[str]:
        """Extract desired image style from text."""
        text_lower = text.lower()
        
        style_keywords = {
            "romantic": "romantic_dinner",
            "elegant": "elegant_plating", 
            "rustic": "rustic_kitchen",
            "restaurant": "restaurant_style",
            "cooking": "cooking_process",
            "close-up": "ingredient_focus",
            "macro": "ingredient_focus"
        }
        
        for keyword, style in style_keywords.items():
            if keyword in text_lower:
                return style
        
        return None
    
    def _determine_priority(self, text: str, content_type: ContentType) -> ProcessingPriority:
        """Determine processing priority based on content."""
        text_lower = text.lower()
        
        # Urgent indicators
        urgent_indicators = ["urgent", "emergency", "now", "immediately", "asap"]
        if any(indicator in text_lower for indicator in urgent_indicators):
            return ProcessingPriority.URGENT
        
        # High priority content types
        high_priority_types = [ContentType.RECIPE_REQUEST, ContentType.COOKING_QUESTION, ContentType.IMAGE_REQUEST]
        if content_type in high_priority_types:
            return ProcessingPriority.HIGH
        
        return ProcessingPriority.NORMAL