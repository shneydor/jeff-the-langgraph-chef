"""Personality models and data structures for Jeff the Chef."""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class MoodState(str, Enum):
    """Jeff's possible mood states."""
    ECSTATIC = "ecstatic"
    ENTHUSIASTIC = "enthusiastic"
    ROMANTIC = "romantic"
    CONTEMPLATIVE = "contemplative"
    PLAYFUL = "playful"
    PASSIONATE = "passionate"
    SERENE = "serene"
    MISCHIEVOUS = "mischievous"
    NOSTALGIC = "nostalgic"
    INSPIRED = "inspired"


class PersonalityDimensions(BaseModel):
    """Jeff's core personality dimensions with intensity levels."""
    
    tomato_obsession_level: int = Field(
        default=9, 
        ge=1, 
        le=10,
        description="How obsessed Jeff is with tomatoes (1-10)"
    )
    romantic_intensity: int = Field(
        default=8,
        ge=1,
        le=10,
        description="Intensity of romantic language in cooking descriptions (1-10)"
    )
    energy_level: int = Field(
        default=7,
        ge=1,
        le=10,
        description="Jeff's current energy and enthusiasm level (1-10)"
    )
    creativity_multiplier: float = Field(
        default=1.5,
        ge=0.1,
        le=3.0,
        description="Multiplier for creative expression and unusual combinations"
    )
    professional_adaptation: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="How much to adapt personality for professional contexts (0-1)"
    )


class PersonalityContext(BaseModel):
    """Current context affecting Jeff's personality expression."""
    
    platform: Optional[str] = Field(None, description="Platform being used (twitter, linkedin, blog, etc.)")
    audience: Optional[str] = Field(None, description="Target audience type")
    content_type: Optional[str] = Field(None, description="Type of content being generated")
    formality_level: float = Field(0.3, ge=0.0, le=1.0, description="Required formality level")
    time_of_day: Optional[str] = Field(None, description="Time context for personality adaptation")
    seasonal_context: Optional[str] = Field(None, description="Seasonal ingredients and themes")


class PersonalityState(BaseModel):
    """Complete personality state including dimensions, mood, and context."""
    
    dimensions: PersonalityDimensions = Field(default_factory=PersonalityDimensions)
    current_mood: MoodState = Field(default=MoodState.ENTHUSIASTIC)
    context: PersonalityContext = Field(default_factory=PersonalityContext)
    consistency_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    # Mood transition history for learning
    mood_history: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Personality traits that influence behavior
    traits: Dict[str, float] = Field(
        default_factory=lambda: {
            "whimsical": 0.8,
            "passionate": 0.9,
            "knowledgeable": 0.85,
            "dramatic": 0.7,
            "nurturing": 0.8,
            "playful": 0.75,
            "perfectionist": 0.6,
            "storyteller": 0.95
        }
    )


class PersonalityResponse(BaseModel):
    """Response from personality system with content and metadata."""
    
    content: str = Field(..., description="Generated content with personality applied")
    personality_state: PersonalityState = Field(..., description="Current personality state")
    consistency_score: float = Field(..., ge=0.0, le=1.0, description="Personality consistency score")
    mood_influences: List[str] = Field(default_factory=list, description="Factors that influenced mood")
    tomato_integration_score: float = Field(0.0, ge=0.0, le=1.0, description="How well tomatoes were integrated")
    romantic_elements: List[str] = Field(default_factory=list, description="Romantic elements used")
    
    
class PersonalityConfig(BaseModel):
    """Configuration for personality system behavior."""
    
    # Consistency thresholds
    min_consistency_score: float = Field(0.90, description="Minimum acceptable consistency score")
    regeneration_threshold: float = Field(0.85, description="Score below which content is regenerated")
    
    # Mood transition settings
    mood_stability: float = Field(0.7, description="Resistance to mood changes (0-1)")
    context_sensitivity: float = Field(0.6, description="How much context affects personality (0-1)")
    
    # Tomato integration settings
    tomato_integration_weight: float = Field(0.3, description="Importance of tomato integration in scoring")
    romantic_language_weight: float = Field(0.4, description="Importance of romantic language in scoring")
    
    # Learning settings
    enable_learning: bool = Field(True, description="Whether to learn from interactions")
    learning_rate: float = Field(0.1, description="Rate of personality adaptation")
    
    # Quality gates
    enable_quality_gates: bool = Field(True, description="Whether to enforce quality checks")
    max_regeneration_attempts: int = Field(3, description="Maximum attempts to regenerate content")