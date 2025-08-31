"""Output Formatter Node for Jeff's LangGraph orchestration system."""

from typing import Dict, Any
from datetime import datetime, timezone

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager
)


class OutputFormatterNode(BaseNode):
    """Formats final output for delivery to user."""
    
    def __init__(self):
        super().__init__("output_formatter")
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Format final output with metadata and presentation."""
        
        content = state.get("selected_variation") or state.get("generated_content", "") or "Oh my darling, it seems my response got lost in the kitchen!"
        
        # Apply formatting based on preferences
        formatted_output = await self._apply_formatting(content, state)
        
        # Add metadata
        output_metadata = self._create_output_metadata(state)
        
        # Finalize workflow
        state = StateManager.finalize_workflow(state, formatted_output)
        state["output_metadata"] = output_metadata
        
        return state
    
    async def _apply_formatting(self, content: str, state: JeffWorkflowState) -> str:
        """Apply output formatting based on preferences."""
        
        format_prefs = state.get("format_preferences", {})
        
        # Basic formatting (could be extended for different platforms)
        formatted = content
        
        # Add chef signature if enabled
        if format_prefs.get("include_signature", True):
            formatted += "\n\n*With culinary love,*\n*Chef Jeff* 🍅❤️"
        
        return formatted
    
    def _create_output_metadata(self, state: JeffWorkflowState) -> Dict[str, Any]:
        """Create metadata about the response."""
        
        personality_state = StateManager.get_personality_state(state)
        quality_results = state.get("quality_check_results", [])
        
        metadata = {
            "generation_timestamp": datetime.now(timezone.utc).isoformat(),
            "workflow_duration": StateManager.calculate_workflow_duration(state),
            "content_type": state.get("content_type"),
            "personality_mood": personality_state.current_mood,
            "quality_score": quality_results[-1].get("score", 0.0) if quality_results else 0.0,
            "regeneration_count": state.get("regeneration_count", 0),
            "tomato_integration_score": quality_results[-1].get("tomato_integration", 0.0) if quality_results else 0.0,
            "romantic_elements_score": quality_results[-1].get("romantic_elements", 0.0) if quality_results else 0.0
        }
        
        return metadata