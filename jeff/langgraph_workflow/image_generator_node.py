"""Image generator node for Jeff's LangGraph workflow."""

import asyncio
from typing import Dict, Any
import structlog

from .base_node import BaseNode
from .state import JeffWorkflowState, StateManager, WorkflowStage, ContentType
from ..image.generator import ImageGenerator
from ..image.models import ImageRequest, ImageStyle

logger = structlog.get_logger(__name__)


class ImageGeneratorNode(BaseNode):
    """Node responsible for generating images using Gemini Flash 2.5."""
    
    def __init__(self):
        super().__init__("image_generator")
        self.image_generator = ImageGenerator()
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Execute image generation logic."""
        
        logger.info(f"Executing {self.node_name}", 
                   session_id=state.get("conversation_context", {}).get("session_id"))
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.PROCESSING)
        
        # Check if this is an image request
        if state.get("content_type") != ContentType.IMAGE_REQUEST:
            logger.debug("Skipping image generation - not an image request")
            return state
        
        # Extract image request from processed input
        image_request_data = await self._extract_image_request(state)
        
        if not image_request_data:
            logger.warning("Could not extract image request data")
            return state
        
        # Create ImageRequest object
        try:
            image_request = ImageRequest(**image_request_data)
        except Exception as e:
            logger.error("Failed to create ImageRequest", error=str(e))
            return state
        
        # Store image request in state
        state["image_request"] = image_request.model_dump()
        
        # Generate image
        logger.info("Generating image with Gemini Flash 2.5", description=image_request.description)
        
        try:
            image_response = await self.image_generator.generate_image(image_request)
            
            # Store image response in state
            state["image_response"] = image_response.model_dump()
            
            # Update generated content with Jeff's commentary
            state["generated_content"] = image_response.jeff_commentary
            
            # Store metadata
            state["image_generation_metadata"] = {
                "generation_time": image_response.generation_time,
                "success": image_response.success,
                "style_applied": image_response.style_applied.value,
                "tomato_integration": image_response.tomato_integration,
                "personality_score": image_response.personality_score,
                "quality_score": image_response.quality_score
            }
            
            logger.info(
                "Image generation completed",
                success=image_response.success,
                generation_time=image_response.generation_time,
                session_id=state.get("conversation_context", {}).get("session_id")
            )
            
        except Exception as e:
            logger.error("Image generation failed", error=str(e))
            
            # Create error response
            state["image_response"] = {
                "success": False,
                "error_message": str(e),
                "jeff_commentary": (
                    "Ah, mon dieu! My artistic vision has encountered a little hiccup, "
                    "like a soufflé that decided to be stubborn! But do not worry, "
                    "ma chérie - Jeff's passion for beautiful food images burns eternal! "
                    "Perhaps we can try again with even more tomato-inspired creativity! 🍅✨"
                )
            }
            
            state["image_generation_metadata"] = {
                "success": False,
                "error": str(e)
            }
        
        return state
    
    async def _extract_image_request(self, state: JeffWorkflowState) -> Dict[str, Any]:
        """Extract image request parameters from processed input."""
        
        processed_input = state.get("processed_input", "")
        extracted_entities = state.get("extracted_entities", {})
        
        # Default image request
        image_request_data = {
            "description": processed_input or "delicious food",
            "style": ImageStyle.FOOD_PHOTOGRAPHY,
            "include_tomatoes": True,  # Jeff always wants tomatoes!
            "session_id": state.get("conversation_context", {}).get("session_id")
        }
        
        # Try to extract more specific image details from entities
        if "image_description" in extracted_entities:
            image_request_data["description"] = extracted_entities["image_description"]
        
        if "image_style" in extracted_entities:
            try:
                style_value = extracted_entities["image_style"].lower().replace(" ", "_")
                if style_value in [s.value for s in ImageStyle]:
                    image_request_data["style"] = ImageStyle(style_value)
            except (ValueError, AttributeError):
                logger.debug("Could not parse image style, using default")
        
        # Check if user specifically doesn't want tomatoes (rare but possible!)
        if processed_input and ("no_tomatoes" in processed_input.lower() or "without tomatoes" in processed_input.lower()):
            image_request_data["include_tomatoes"] = False
            logger.info("User specifically requested no tomatoes - Jeff is heartbroken but compliant!")
        
        return image_request_data