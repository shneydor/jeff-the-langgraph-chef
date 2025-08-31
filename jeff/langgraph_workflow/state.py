"""LangGraph state management for Jeff the Chef's workflow orchestration."""

from typing import Dict, List, Optional, Any, Union, TypedDict, Annotated
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field

from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from ..personality.models import PersonalityState, PersonalityContext
from ..core.config import settings


class WorkflowStage(str, Enum):
    """Current stage in the workflow processing."""
    INPUT_RECEIVED = "input_received"
    PERSONALITY_APPLIED = "personality_applied"
    CONTENT_ROUTED = "content_routed"
    PROCESSING = "processing"
    QUALITY_CHECKED = "quality_checked"
    OUTPUT_FORMATTED = "output_formatted"
    COMPLETED = "completed"
    ERROR = "error"


class ContentType(str, Enum):
    """Types of content Jeff can process."""
    RECIPE_REQUEST = "recipe_request"
    COOKING_QUESTION = "cooking_question"
    INGREDIENT_INQUIRY = "ingredient_inquiry"
    TECHNIQUE_QUESTION = "technique_question"
    GENERAL_CHAT = "general_chat"
    RECIPE_REVIEW = "recipe_review"
    MEAL_PLANNING = "meal_planning"
    FOOD_PAIRING = "food_pairing"
    NUTRITION_QUESTION = "nutrition_question"
    COOKING_TIPS = "cooking_tips"


class ProcessingPriority(str, Enum):
    """Priority levels for processing requests."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class QualityCheckResult(BaseModel):
    """Result of quality assurance checks."""
    passed: bool = Field(..., description="Whether quality check passed")
    score: float = Field(..., ge=0.0, le=1.0, description="Quality score")
    issues: List[str] = Field(default_factory=list, description="Quality issues found")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    personality_consistency: float = Field(..., ge=0.0, le=1.0, description="Personality consistency score")
    tomato_integration: float = Field(0.0, ge=0.0, le=1.0, description="Tomato integration score")
    romantic_elements: float = Field(0.0, ge=0.0, le=1.0, description="Romantic language score")


class WorkflowMetrics(BaseModel):
    """Metrics tracking for workflow performance."""
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    processing_time: Optional[float] = None
    stage_durations: Dict[str, float] = Field(default_factory=dict)
    node_call_count: Dict[str, int] = Field(default_factory=dict)
    quality_scores: List[float] = Field(default_factory=list)
    retry_count: int = 0
    error_count: int = 0


class ConversationContext(BaseModel):
    """Context about the ongoing conversation."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier if available")
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list, description="Previous interactions")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences and dietary restrictions")
    recipe_history: List[str] = Field(default_factory=list, description="Previously discussed recipes")
    ingredient_preferences: Dict[str, float] = Field(default_factory=dict, description="User ingredient preferences (-1 to 1)")
    dietary_restrictions: List[str] = Field(default_factory=list, description="User dietary restrictions")
    skill_level: str = Field("intermediate", description="User's cooking skill level")
    favorite_cuisines: List[str] = Field(default_factory=list, description="User's favorite cuisines")
    kitchen_equipment: List[str] = Field(default_factory=list, description="Available kitchen equipment")


class ProcessingError(BaseModel):
    """Information about processing errors."""
    error_type: str = Field(..., description="Type of error")
    error_message: str = Field(..., description="Error message")
    node_name: str = Field(..., description="Node where error occurred")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retry_count: int = Field(0, description="Number of retries attempted")
    recoverable: bool = Field(True, description="Whether error is recoverable")
    recovery_strategy: Optional[str] = Field(None, description="Suggested recovery strategy")


class NodeExecutionInfo(BaseModel):
    """Information about node execution."""
    node_name: str = Field(..., description="Name of the executed node")  
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    success: bool = True
    output_size: int = 0
    confidence_score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# LangGraph State Type Definition
class JeffWorkflowState(TypedDict):
    """Main state type for Jeff's LangGraph workflow."""
    
    # Core message handling
    messages: Annotated[List[BaseMessage], add_messages]
    
    # Workflow control
    current_stage: WorkflowStage
    content_type: Optional[ContentType]
    processing_priority: ProcessingPriority
    workflow_complete: bool
    
    # Input processing
    raw_input: str
    processed_input: Optional[str]
    extracted_entities: Dict[str, Any]
    user_intent: Optional[str]
    confidence_score: float
    
    # Personality system
    personality_state: Dict[str, Any]  # Serialized PersonalityState
    personality_context: Dict[str, Any]  # Serialized PersonalityContext
    personality_response: Optional[Dict[str, Any]]
    
    # Content generation
    generated_content: Optional[str]
    content_variations: List[str]
    selected_variation: Optional[str]
    
    # Recipe-specific data
    recipe_data: Optional[Dict[str, Any]]
    ingredients_list: List[str]
    cooking_techniques: List[str]
    dietary_adaptations: List[str]
    nutritional_info: Optional[Dict[str, Any]]
    
    # Quality assurance
    quality_check_results: List[Dict[str, Any]]  # Serialized QualityCheckResult
    regeneration_count: int
    quality_passed: bool
    
    # Context and conversation
    conversation_context: Dict[str, Any]  # Serialized ConversationContext
    session_metadata: Dict[str, Any]
    
    # Workflow metrics and monitoring
    workflow_metrics: Dict[str, Any]  # Serialized WorkflowMetrics
    node_execution_history: List[Dict[str, Any]]  # Serialized NodeExecutionInfo list
    
    # Error handling
    errors: List[Dict[str, Any]]  # Serialized ProcessingError list
    last_error: Optional[Dict[str, Any]]
    recovery_attempts: int
    
    # Output formatting
    final_output: Optional[str]
    output_metadata: Dict[str, Any]
    format_preferences: Dict[str, Any]
    
    # Feature flags and configuration
    features_enabled: Dict[str, bool]
    processing_config: Dict[str, Any]
    debug_info: Dict[str, Any]


class StateManager:
    """Manager for LangGraph state operations and utilities."""
    
    @staticmethod
    def create_initial_state(
        user_input: str,
        session_id: str,
        user_id: Optional[str] = None,
        personality_context: Optional[PersonalityContext] = None
    ) -> JeffWorkflowState:
        """Create initial workflow state from user input."""
        
        # Initialize conversation context
        conversation_context = ConversationContext(
            session_id=session_id,
            user_id=user_id
        )
        
        # Initialize personality state
        personality_state = PersonalityState()
        if personality_context:
            personality_state.context = personality_context
        
        # Initialize workflow metrics
        workflow_metrics = WorkflowMetrics()
        
        # Create initial state
        state: JeffWorkflowState = {
            # Core messages
            "messages": [HumanMessage(content=user_input)],
            
            # Workflow control
            "current_stage": WorkflowStage.INPUT_RECEIVED,
            "content_type": None,
            "processing_priority": ProcessingPriority.NORMAL,
            "workflow_complete": False,
            
            # Input processing
            "raw_input": user_input,
            "processed_input": None,
            "extracted_entities": {},
            "user_intent": None,
            "confidence_score": 0.0,
            
            # Personality system
            "personality_state": personality_state.model_dump(),
            "personality_context": personality_context.model_dump() if personality_context else {},
            "personality_response": None,
            
            # Content generation
            "generated_content": None,
            "content_variations": [],
            "selected_variation": None,
            
            # Recipe-specific data
            "recipe_data": None,
            "ingredients_list": [],
            "cooking_techniques": [],
            "dietary_adaptations": [],
            "nutritional_info": None,
            
            # Quality assurance
            "quality_check_results": [],
            "regeneration_count": 0,
            "quality_passed": False,
            
            # Context and conversation
            "conversation_context": conversation_context.model_dump(),
            "session_metadata": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat()
            },
            
            # Workflow metrics
            "workflow_metrics": workflow_metrics.model_dump(),
            "node_execution_history": [],
            
            # Error handling
            "errors": [],
            "last_error": None,
            "recovery_attempts": 0,
            
            # Output formatting
            "final_output": None,
            "output_metadata": {},
            "format_preferences": {},
            
            # Feature flags
            "features_enabled": {
                "memory_system": settings.enable_memory_system,
                "image_generation": settings.enable_image_generation,
                "multi_platform": settings.enable_multi_platform,
                "quality_gates": True,
                "tomato_integration": True,
                "romantic_writing": True
            },
            "processing_config": {
                "max_regeneration_attempts": 3,
                "quality_threshold": settings.personality_consistency_threshold,
                "response_time_limit": settings.response_time_threshold,
                "enable_debug": settings.debug
            },
            "debug_info": {}
        }
        
        return state
    
    @staticmethod
    def update_stage(state: JeffWorkflowState, new_stage: WorkflowStage) -> JeffWorkflowState:
        """Update workflow stage and related timestamps."""
        old_stage = state["current_stage"]
        state["current_stage"] = new_stage
        
        # Update metrics
        current_time = datetime.now(timezone.utc)
        if "workflow_metrics" in state and state["workflow_metrics"]:
            metrics_data = state["workflow_metrics"]
            if old_stage and "stage_durations" in metrics_data:
                # Calculate duration of previous stage
                start_time_str = metrics_data.get("start_time", current_time.isoformat())
                start_time = datetime.fromisoformat(start_time_str) if isinstance(start_time_str, str) else start_time_str
                duration = (current_time - start_time).total_seconds()
                metrics_data["stage_durations"][old_stage] = duration
        
        # Update session metadata
        state["session_metadata"]["last_updated"] = current_time.isoformat()
        
        return state
    
    @staticmethod
    def add_error(state: JeffWorkflowState, error: ProcessingError) -> JeffWorkflowState:
        """Add error to state."""
        error_dict = error.model_dump()
        error_dict["timestamp"] = error_dict["timestamp"].isoformat()
        
        state["errors"].append(error_dict)
        state["last_error"] = error_dict
        state["current_stage"] = WorkflowStage.ERROR
        
        # Update error count in metrics
        if "workflow_metrics" in state and state["workflow_metrics"]:
            state["workflow_metrics"]["error_count"] += 1
        
        return state
    
    @staticmethod
    def add_quality_check(state: JeffWorkflowState, quality_result: QualityCheckResult) -> JeffWorkflowState:
        """Add quality check result to state."""
        quality_dict = quality_result.model_dump()
        state["quality_check_results"].append(quality_dict)
        state["quality_passed"] = quality_result.passed
        
        # Update metrics
        if "workflow_metrics" in state and state["workflow_metrics"]:
            state["workflow_metrics"]["quality_scores"].append(quality_result.score)
        
        return state
    
    @staticmethod
    def record_node_execution(
        state: JeffWorkflowState, 
        node_info: NodeExecutionInfo
    ) -> JeffWorkflowState:
        """Record node execution information."""
        # Convert datetime fields to ISO strings for serialization
        node_dict = node_info.model_dump()
        node_dict["start_time"] = node_info.start_time.isoformat()
        if node_info.end_time:
            node_dict["end_time"] = node_info.end_time.isoformat()
        
        state["node_execution_history"].append(node_dict)
        
        # Update node call count in metrics
        if "workflow_metrics" in state and state["workflow_metrics"]:
            node_counts = state["workflow_metrics"]["node_call_count"]
            node_counts[node_info.node_name] = node_counts.get(node_info.node_name, 0) + 1
        
        return state
    
    @staticmethod
    def get_personality_state(state: JeffWorkflowState) -> PersonalityState:
        """Extract PersonalityState from workflow state."""
        personality_data = state.get("personality_state", {})
        return PersonalityState.model_validate(personality_data)
    
    @staticmethod
    def update_personality_state(
        state: JeffWorkflowState, 
        personality_state: PersonalityState
    ) -> JeffWorkflowState:
        """Update personality state in workflow state."""
        state["personality_state"] = personality_state.model_dump()
        return state
    
    @staticmethod
    def get_conversation_context(state: JeffWorkflowState) -> ConversationContext:
        """Extract ConversationContext from workflow state."""
        context_data = state.get("conversation_context", {})
        return ConversationContext.model_validate(context_data)
    
    @staticmethod
    def update_conversation_context(
        state: JeffWorkflowState,
        conversation_context: ConversationContext
    ) -> JeffWorkflowState:
        """Update conversation context in workflow state."""
        state["conversation_context"] = conversation_context.model_dump()
        return state
    
    @staticmethod
    def is_regeneration_needed(state: JeffWorkflowState) -> bool:
        """Check if content regeneration is needed based on quality."""
        if not state.get("quality_check_results"):
            return True
        
        latest_quality = state["quality_check_results"][-1]
        threshold = state["processing_config"].get("quality_threshold", 0.85)
        max_attempts = state["processing_config"].get("max_regeneration_attempts", 3)
        
        return (
            not latest_quality.get("passed", False) and 
            state.get("regeneration_count", 0) < max_attempts
        )
    
    @staticmethod
    def calculate_workflow_duration(state: JeffWorkflowState) -> Optional[float]:
        """Calculate total workflow duration."""
        metrics = state.get("workflow_metrics", {})
        start_time_str = metrics.get("start_time")
        end_time_str = metrics.get("end_time")
        
        if start_time_str and end_time_str:
            start_time = datetime.fromisoformat(start_time_str) if isinstance(start_time_str, str) else start_time_str
            end_time = datetime.fromisoformat(end_time_str) if isinstance(end_time_str, str) else end_time_str
            return (end_time - start_time).total_seconds()
        
        return None
    
    @staticmethod
    def finalize_workflow(state: JeffWorkflowState, final_output: str) -> JeffWorkflowState:
        """Finalize workflow with output and metrics."""
        current_time = datetime.now(timezone.utc)
        
        # Set final output
        state["final_output"] = final_output
        state["workflow_complete"] = True
        state["current_stage"] = WorkflowStage.COMPLETED
        
        # Update metrics
        if "workflow_metrics" in state and state["workflow_metrics"]:
            metrics = state["workflow_metrics"]
            metrics["end_time"] = current_time.isoformat()
            
            # Calculate total processing time
            start_time_str = metrics.get("start_time", current_time.isoformat())
            start_time = datetime.fromisoformat(start_time_str) if isinstance(start_time_str, str) else start_time_str
            metrics["processing_time"] = (current_time - start_time).total_seconds()
        
        # Add final AI message
        state["messages"].append(AIMessage(content=final_output))
        
        return state
    
    @staticmethod
    def get_debug_summary(state: JeffWorkflowState) -> Dict[str, Any]:
        """Get debug summary of workflow state."""
        return {
            "current_stage": state.get("current_stage"),
            "workflow_complete": state.get("workflow_complete"),
            "content_type": state.get("content_type"),
            "quality_passed": state.get("quality_passed"),
            "regeneration_count": state.get("regeneration_count"),
            "error_count": len(state.get("errors", [])),
            "node_executions": len(state.get("node_execution_history", [])),
            "processing_time": StateManager.calculate_workflow_duration(state),
            "personality_consistency": state.get("personality_state", {}).get("consistency_score"),
            "features_enabled": state.get("features_enabled", {})
        }