"""Content Router Node for Jeff's LangGraph orchestration system."""

from typing import Dict, Optional, Any

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage, 
    ContentType
)


class ContentRouterNode(BaseNode):
    """Routes content to appropriate processing based on type and context."""
    
    def __init__(self):
        super().__init__("content_router")
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Route content based on type and determine next processing steps."""
        
        content_type = state.get("content_type")
        confidence = state.get("confidence_score", 0.0)
        
        # Determine routing decision
        routing_decision = self._make_routing_decision(content_type, confidence, state)
        
        # Update state with routing information
        state["routing_decision"] = routing_decision
        state["next_nodes"] = routing_decision.get("next_nodes", ["response_generator"])
        
        # Set processing flags based on content type
        processing_flags = self._set_processing_flags(content_type, state)
        state["processing_flags"] = processing_flags
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.PROCESSING)
        
        return state
    
    def _make_routing_decision(
        self, 
        content_type: Optional[ContentType], 
        confidence: float,
        state: JeffWorkflowState
    ) -> Dict[str, Any]:
        """Make routing decision based on content analysis."""
        
        routing_decision = {
            "primary_path": "general_response",
            "next_nodes": ["response_generator"],
            "requires_recipe_generation": False,
            "requires_knowledge_lookup": False,
            "requires_special_processing": False
        }
        
        if not content_type:
            return routing_decision
        
        # Route based on content type
        if content_type == ContentType.RECIPE_REQUEST:
            routing_decision.update({
                "primary_path": "recipe_generation",
                "next_nodes": ["recipe_generator", "romantic_enhancer"],
                "requires_recipe_generation": True,
                "requires_knowledge_lookup": True
            })
        
        elif content_type in [ContentType.COOKING_QUESTION, ContentType.TECHNIQUE_QUESTION]:
            routing_decision.update({
                "primary_path": "knowledge_response",
                "next_nodes": ["knowledge_processor", "response_generator"],
                "requires_knowledge_lookup": True
            })
        
        elif content_type == ContentType.INGREDIENT_INQUIRY:
            routing_decision.update({
                "primary_path": "ingredient_analysis",
                "next_nodes": ["ingredient_processor", "tomato_enhancer"],
                "requires_knowledge_lookup": True,
                "requires_special_processing": True
            })
        
        elif content_type == ContentType.FOOD_PAIRING:
            routing_decision.update({
                "primary_path": "pairing_analysis",
                "next_nodes": ["pairing_processor", "tomato_enhancer"],
                "requires_knowledge_lookup": True
            })
        
        # Adjust based on confidence level
        if confidence < 0.5:
            routing_decision["next_nodes"].append("clarification_generator")
        
        return routing_decision
    
    def _set_processing_flags(self, content_type: Optional[ContentType], state: JeffWorkflowState) -> Dict[str, bool]:
        """Set processing flags based on content type and features."""
        
        features_enabled = state.get("features_enabled", {})
        
        flags = {
            "apply_romantic_writing": features_enabled.get("romantic_writing", True),
            "integrate_tomatoes": features_enabled.get("tomato_integration", True),
            "use_memory_system": features_enabled.get("memory_system", False),
            "generate_images": False,  # Will be enabled for recipe requests
            "multi_platform_adapt": features_enabled.get("multi_platform", False),
            "quality_gate_required": features_enabled.get("quality_gates", True)
        }
        
        # Content-specific flag adjustments
        if content_type == ContentType.RECIPE_REQUEST:
            flags["generate_images"] = features_enabled.get("image_generation", False)
            flags["apply_romantic_writing"] = True
            flags["integrate_tomatoes"] = True
        
        elif content_type == ContentType.GENERAL_CHAT:
            flags["integrate_tomatoes"] = state.get("personality_state", {}).get("dimensions", {}).get("tomato_obsession_level", 9) >= 7
        
        return flags