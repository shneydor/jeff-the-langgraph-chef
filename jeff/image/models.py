"""Data models for Jeff's image generation system."""

from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ImageStyle(str, Enum):
    """Available image generation styles."""
    FOOD_PHOTOGRAPHY = "food_photography"
    ROMANTIC_DINNER = "romantic_dinner"
    RUSTIC_KITCHEN = "rustic_kitchen"
    ELEGANT_PLATING = "elegant_plating"
    COOKING_PROCESS = "cooking_process"
    INGREDIENT_FOCUS = "ingredient_focus"
    RESTAURANT_STYLE = "restaurant_style"


class ImageRequest(BaseModel):
    """Request model for image generation."""
    description: str = Field(..., description="Description of the image to generate")
    style: ImageStyle = Field(ImageStyle.FOOD_PHOTOGRAPHY, description="Image style")
    include_tomatoes: bool = Field(True, description="Whether to include tomatoes in the image")
    session_id: Optional[str] = Field(None, description="Session ID for context")
    
    @validator('description')
    def description_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Description cannot be empty')
        if len(v) > 500:
            raise ValueError('Description too long (max 500 characters)')
        return v.strip()


class ImageResponse(BaseModel):
    """Response model for generated images."""
    image_url: Optional[str] = Field(None, description="URL to the generated image")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image data")
    jeff_commentary: str = Field(..., description="Jeff's romantic commentary about the image")
    generation_time: float = Field(..., description="Time taken to generate the image")
    prompt_used: str = Field(..., description="The actual prompt sent to Gemini")
    success: bool = Field(..., description="Whether generation was successful")
    error_message: Optional[str] = Field(None, description="Error message if generation failed")
    
    # Metadata
    style_applied: ImageStyle = Field(..., description="Style that was applied")
    tomato_integration: bool = Field(..., description="Whether tomatoes were included")
    personality_score: Optional[float] = Field(None, description="Jeff's personality consistency in commentary")
    quality_score: Optional[float] = Field(None, description="Overall quality assessment")


class ImageGenerationMetrics(BaseModel):
    """Metrics for image generation performance."""
    total_requests: int = Field(0, description="Total image generation requests")
    successful_generations: int = Field(0, description="Successful image generations")
    failed_generations: int = Field(0, description="Failed image generations")
    average_generation_time: float = Field(0.0, description="Average generation time in seconds")
    tomato_integration_rate: float = Field(0.0, description="Rate of tomato integration")
    personality_consistency_score: float = Field(0.0, description="Average personality consistency")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last metrics update")


class ImagePromptTemplate(BaseModel):
    """Template for generating Gemini prompts."""
    base_template: str = Field(..., description="Base prompt template")
    style_modifiers: Dict[ImageStyle, str] = Field(..., description="Style-specific modifications")
    tomato_integration_phrases: List[str] = Field(..., description="Phrases for tomato integration")
    romantic_elements: List[str] = Field(..., description="Romantic language elements")
    jeff_signature_elements: List[str] = Field(..., description="Jeff's signature visual elements")