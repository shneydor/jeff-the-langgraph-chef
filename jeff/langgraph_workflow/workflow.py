"""Main LangGraph workflow orchestration for Jeff the Chef."""

from typing import Dict, List, Optional, Any, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import JeffWorkflowState, StateManager, WorkflowStage, ContentType
from .nodes import (
    InputProcessorNode,
    PersonalityFilterNode, 
    ContentRouterNode,
    ResponseGeneratorNode,
    QualityValidatorNode,
    OutputFormatterNode
)


class JeffWorkflowOrchestrator:
    """Main orchestrator for Jeff's LangGraph workflow."""
    
    def __init__(self):
        self.memory = MemorySaver()
        self.nodes = self._initialize_nodes()
        self.workflow = self._build_workflow()
        
    def _initialize_nodes(self) -> Dict[str, Any]:
        """Initialize all workflow nodes."""
        return {
            "input_processor": InputProcessorNode(),
            "personality_filter": PersonalityFilterNode(),
            "content_router": ContentRouterNode(),
            "response_generator": ResponseGeneratorNode(),
            "quality_validator": QualityValidatorNode(),
            "output_formatter": OutputFormatterNode()
        }
    
    def _build_workflow(self) -> StateGraph:
        """Build the complete LangGraph workflow with conditional routing."""
        
        # Create workflow graph
        workflow = StateGraph(JeffWorkflowState)
        
        # Add nodes
        workflow.add_node("input_processor", self.nodes["input_processor"].execute)
        workflow.add_node("personality_filter", self.nodes["personality_filter"].execute)
        workflow.add_node("content_router", self.nodes["content_router"].execute)
        workflow.add_node("response_generator", self.nodes["response_generator"].execute)
        workflow.add_node("quality_validator", self.nodes["quality_validator"].execute)
        workflow.add_node("output_formatter", self.nodes["output_formatter"].execute)
        
        # Set entry point
        workflow.set_entry_point("input_processor")
        
        # Add edges with conditional routing
        workflow.add_edge("input_processor", "personality_filter")
        workflow.add_edge("personality_filter", "content_router")
        
        # Content router to appropriate processing
        workflow.add_conditional_edges(
            "content_router",
            self._route_content,
            {
                "recipe_generation": "response_generator",  # Would route to recipe nodes in full implementation
                "general_response": "response_generator",
                "knowledge_response": "response_generator",
                "error_handling": "output_formatter"
            }
        )
        
        # Response generation to quality validation
        workflow.add_edge("response_generator", "quality_validator")
        
        # Quality validator with regeneration logic
        workflow.add_conditional_edges(
            "quality_validator",
            self._check_quality_gate,
            {
                "regenerate": "response_generator",
                "format_output": "output_formatter",
                "error": "output_formatter"
            }
        )
        
        # Output formatter to end
        workflow.add_edge("output_formatter", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    def _route_content(self, state: JeffWorkflowState) -> str:
        """Route content based on analysis results."""
        
        # Check for errors first
        if state.get("current_stage") == WorkflowStage.ERROR:
            return "error_handling"
        
        # Route based on content type and routing decision
        routing_decision = state.get("routing_decision", {})
        primary_path = routing_decision.get("primary_path", "general_response")
        
        # Map routing paths to actual routes
        route_mapping = {
            "recipe_generation": "recipe_generation",
            "knowledge_response": "general_response", 
            "ingredient_analysis": "general_response",
            "pairing_analysis": "general_response",
            "general_response": "general_response"
        }
        
        return route_mapping.get(primary_path, "general_response")
    
    def _check_quality_gate(self, state: JeffWorkflowState) -> str:
        """Check quality gate and decide next step."""
        
        # Check for errors
        if state.get("current_stage") == WorkflowStage.ERROR:
            return "error"
        
        # Check if regeneration is needed
        if StateManager.is_regeneration_needed(state):
            max_attempts = state.get("processing_config", {}).get("max_regeneration_attempts", 3)
            current_attempts = state.get("regeneration_count", 0)
            
            if current_attempts < max_attempts:
                return "regenerate"
            else:
                # Max attempts reached, proceed with current content
                return "format_output"
        
        # Quality check passed
        return "format_output"
    
    async def process_user_input(
        self,
        user_input: str,
        session_id: str,
        user_id: Optional[str] = None,
        format_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process user input through the complete workflow."""
        
        # Create initial state
        initial_state = StateManager.create_initial_state(
            user_input=user_input,
            session_id=session_id,
            user_id=user_id
        )
        
        # Add format preferences if provided
        if format_preferences:
            initial_state["format_preferences"] = format_preferences
        
        # Execute workflow
        try:
            final_state = await self.workflow.ainvoke(
                initial_state,
                config={"configurable": {"thread_id": session_id}}
            )
            
            # Extract results
            result = {
                "response": final_state.get("final_output", ""),
                "metadata": final_state.get("output_metadata", {}),
                "session_id": session_id,
                "success": final_state.get("workflow_complete", False),
                "error": final_state.get("last_error"),
                "debug_info": StateManager.get_debug_summary(final_state) if initial_state.get("processing_config", {}).get("enable_debug", False) else None
            }
            
            return result
            
        except Exception as e:
            return {
                "response": "Oh my stars! Something went terribly wrong in my kitchen! Let me try again...",
                "metadata": {"error": str(e)},
                "session_id": session_id,
                "success": False,
                "error": {"error_type": type(e).__name__, "error_message": str(e)}
            }
    
    async def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        try:
            # Get state from memory
            state = await self.workflow.aget_state(
                config={"configurable": {"thread_id": session_id}}
            )
            
            if state and state.values:
                messages = state.values.get("messages", [])
                return [
                    {
                        "type": msg.type,
                        "content": msg.content,
                        "timestamp": getattr(msg, "timestamp", None)
                    }
                    for msg in messages
                ]
            
            return []
            
        except Exception:
            return []
    
    async def update_user_preferences(
        self,
        session_id: str,
        preferences: Dict[str, Any]
    ) -> bool:
        """Update user preferences for a session."""
        try:
            # Get current state
            state = await self.workflow.aget_state(
                config={"configurable": {"thread_id": session_id}}
            )
            
            if state and state.values:
                # Update conversation context with preferences
                conversation_context = StateManager.get_conversation_context(state.values)
                conversation_context.user_preferences.update(preferences)
                
                # Update dietary restrictions if provided
                if "dietary_restrictions" in preferences:
                    conversation_context.dietary_restrictions = preferences["dietary_restrictions"]
                
                # Update skill level if provided
                if "skill_level" in preferences:
                    conversation_context.skill_level = preferences["skill_level"]
                
                # Update ingredient preferences if provided
                if "ingredient_preferences" in preferences:
                    conversation_context.ingredient_preferences.update(preferences["ingredient_preferences"])
                
                # Save updated state
                updated_state = StateManager.update_conversation_context(state.values, conversation_context)
                
                # This would need to be implemented based on LangGraph's state update mechanism
                # For now, return True indicating success
                return True
            
            return False
            
        except Exception:
            return False
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get statistics about workflow performance."""
        # This would typically come from monitoring/metrics system
        return {
            "total_conversations": 0,  # Would be tracked
            "average_response_time": 0.0,
            "quality_score_average": 0.0,
            "personality_consistency_average": 0.0,
            "tomato_integration_average": 0.0,
            "error_rate": 0.0,
            "regeneration_rate": 0.0
        }


# Conditional routing functions for advanced workflow control
class ConditionalRouter:
    """Advanced conditional routing logic for complex workflow decisions."""
    
    @staticmethod
    def should_generate_recipe(state: JeffWorkflowState) -> bool:
        """Determine if recipe generation is needed."""
        content_type = state.get("content_type")
        entities = state.get("extracted_entities", {})
        
        return (
            content_type == ContentType.RECIPE_REQUEST or
            (content_type == ContentType.COOKING_QUESTION and 
             len(entities.get("ingredients", [])) >= 3)
        )
    
    @staticmethod
    def requires_knowledge_lookup(state: JeffWorkflowState) -> bool:
        """Determine if knowledge base lookup is needed."""
        content_type = state.get("content_type")
        
        knowledge_requiring_types = [
            ContentType.COOKING_QUESTION,
            ContentType.TECHNIQUE_QUESTION,
            ContentType.INGREDIENT_INQUIRY,
            ContentType.NUTRITION_QUESTION,
            ContentType.FOOD_PAIRING
        ]
        
        return content_type in knowledge_requiring_types
    
    @staticmethod
    def needs_tomato_enhancement(state: JeffWorkflowState) -> bool:
        """Determine if tomato enhancement is needed."""
        personality_state = StateManager.get_personality_state(state)
        obsession_level = personality_state.dimensions.tomato_obsession_level
        
        # Always enhance if obsession level is high
        if obsession_level >= 8:
            return True
        
        # Check if tomatoes are already mentioned
        content = state.get("generated_content", "")
        if "tomato" in content.lower():
            return False
        
        # Enhance based on content type and obsession level
        content_type = state.get("content_type")
        if content_type in [ContentType.RECIPE_REQUEST, ContentType.INGREDIENT_INQUIRY]:
            return obsession_level >= 6
        
        return obsession_level >= 9  # Very high obsession for other content types
    
    @staticmethod
    def requires_clarification(state: JeffWorkflowState) -> bool:
        """Determine if clarification is needed from user."""
        confidence = state.get("confidence_score", 1.0)
        entities = state.get("extracted_entities", {})
        
        # Low confidence score
        if confidence < 0.4:
            return True
        
        # Recipe request without enough information
        content_type = state.get("content_type")
        if content_type == ContentType.RECIPE_REQUEST:
            if not entities.get("ingredients") and not entities.get("cuisine_types"):
                return True
        
        return False
    
    @staticmethod
    def should_use_memory(state: JeffWorkflowState) -> bool:
        """Determine if memory system should be used."""
        features_enabled = state.get("features_enabled", {})
        if not features_enabled.get("memory_system", False):
            return False
        
        # Use memory for ongoing conversations
        conversation_context = StateManager.get_conversation_context(state)
        return len(conversation_context.conversation_history) > 0
    
    @staticmethod
    def priority_processing_needed(state: JeffWorkflowState) -> bool:
        """Determine if priority processing is needed."""
        priority = state.get("processing_priority")
        return priority in ["urgent", "high"]


# Quality gate implementations
class QualityGates:
    """Quality gate implementations for various content types."""
    
    @staticmethod
    def personality_consistency_gate(state: JeffWorkflowState, threshold: float = 0.85) -> bool:
        """Check if personality consistency meets threshold."""
        quality_results = state.get("quality_check_results", [])
        if not quality_results:
            return False
        
        latest_result = quality_results[-1]
        return latest_result.get("personality_consistency", 0.0) >= threshold
    
    @staticmethod
    def tomato_integration_gate(state: JeffWorkflowState, threshold: float = 0.3) -> bool:
        """Check if tomato integration meets obsession level requirements."""
        personality_state = StateManager.get_personality_state(state)
        obsession_level = personality_state.dimensions.tomato_obsession_level
        
        # Scale threshold by obsession level
        required_threshold = threshold * (obsession_level / 10.0)
        
        quality_results = state.get("quality_check_results", [])
        if not quality_results:
            return obsession_level < 7  # Low obsession doesn't require tomato integration
        
        latest_result = quality_results[-1]
        actual_score = latest_result.get("tomato_integration", 0.0)
        
        return actual_score >= required_threshold
    
    @staticmethod
    def romantic_language_gate(state: JeffWorkflowState, threshold: float = 0.4) -> bool:
        """Check if romantic language meets intensity requirements."""
        personality_state = StateManager.get_personality_state(state)
        romantic_intensity = personality_state.dimensions.romantic_intensity
        
        # Scale threshold by romantic intensity
        required_threshold = threshold * (romantic_intensity / 10.0)
        
        quality_results = state.get("quality_check_results", [])
        if not quality_results:
            return romantic_intensity < 6  # Low intensity doesn't require romantic language
        
        latest_result = quality_results[-1]
        actual_score = latest_result.get("romantic_elements", 0.0)
        
        return actual_score >= required_threshold
    
    @staticmethod
    def overall_quality_gate(state: JeffWorkflowState) -> bool:
        """Check overall quality against all gates."""
        gates = [
            QualityGates.personality_consistency_gate(state),
            QualityGates.tomato_integration_gate(state),
            QualityGates.romantic_language_gate(state)
        ]
        
        # Require at least 2 out of 3 gates to pass
        return sum(gates) >= 2
    
    @staticmethod
    def content_appropriateness_gate(state: JeffWorkflowState) -> bool:
        """Check if content is appropriate for the context."""
        content = state.get("generated_content", "")
        
        # Basic appropriateness checks
        inappropriate_terms = ["offensive", "inappropriate", "harmful"]  # Would be more comprehensive
        
        content_lower = content.lower()
        for term in inappropriate_terms:
            if term in content_lower:
                return False
        
        # Check length appropriateness
        content_type = state.get("content_type")
        if content_type == ContentType.GENERAL_CHAT and len(content) > 1000:
            return False  # Too long for general chat
        
        return True