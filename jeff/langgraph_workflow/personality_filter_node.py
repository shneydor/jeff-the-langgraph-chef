"""Personality Filter Node for Jeff's LangGraph orchestration system."""

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage
)
from ..personality.engine import PersonalityEngine
from ..personality.models import PersonalityContext


class PersonalityFilterNode(BaseNode):
    """Applies Jeff's personality context to the processing pipeline."""
    
    def __init__(self):
        super().__init__("personality_filter")
        self.personality_engine = PersonalityEngine()
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Apply personality context and mood analysis."""
        
        # Get current personality state
        personality_state = StateManager.get_personality_state(state)
        
        # Create personality context based on detected content type
        context = PersonalityContext(
            platform=state.get("format_preferences", {}).get("platform", "chat"),
            content_type=state.get("content_type"),
            formality_level=0.3  # Default casual level for Jeff
        )
        
        # Update personality context
        personality_state.context = context
        
        # Analyze input for mood triggers and update personality
        processed_input = state.get("processed_input", "")
        personality_response = await self.personality_engine.process_input(
            processed_input, 
            context
        )
        
        # Update state with personality information
        state = StateManager.update_personality_state(state, personality_response.personality_state)
        state["personality_response"] = personality_response.model_dump()
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.CONTENT_ROUTED)
        
        return state