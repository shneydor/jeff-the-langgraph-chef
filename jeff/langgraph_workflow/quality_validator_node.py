"""Quality Validator Node for Jeff's LangGraph orchestration system."""

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage, 
    QualityCheckResult
)
from ..personality.engine import PersonalityEngine
from ..personality.tomato_integration import TomatoIntegrationEngine


class QualityValidatorNode(BaseNode):
    """Validates response quality and personality consistency."""
    
    def __init__(self):
        super().__init__("quality_validator")
        self.personality_engine = PersonalityEngine()
        self.tomato_engine = TomatoIntegrationEngine()
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Validate quality of generated content."""
        
        generated_content = state.get("generated_content", "")
        personality_state = StateManager.get_personality_state(state)
        
        # Perform quality checks
        quality_result = await self._perform_quality_checks(
            generated_content,
            personality_state,
            state
        )
        
        # Add quality check to state
        state = StateManager.add_quality_check(state, quality_result)
        
        # Determine if regeneration is needed
        if StateManager.is_regeneration_needed(state):
            state["regeneration_count"] = state.get("regeneration_count", 0) + 1
            # Would route back for regeneration
            state = StateManager.update_stage(state, WorkflowStage.PROCESSING)
        else:
            state = StateManager.update_stage(state, WorkflowStage.OUTPUT_FORMATTED)
        
        return state
    
    async def _perform_quality_checks(
        self,
        content: str,
        personality_state,
        state: JeffWorkflowState
    ) -> QualityCheckResult:
        """Perform comprehensive quality assessment."""
        
        # Calculate personality consistency
        personality_score = await self.personality_engine._calculate_consistency_score(content)
        
        # Calculate tomato integration score
        tomato_score = self.tomato_engine.evaluate_tomato_integration_success(
            content,
            personality_state.dimensions.tomato_obsession_level
        )
        
        # Calculate romantic elements score
        romantic_elements = self.personality_engine._extract_romantic_elements(content)
        romantic_score = len(romantic_elements) / 10.0  # Normalize to 0-1
        
        # Overall quality score (weighted average)
        weights = state.get("processing_config", {})
        personality_weight = weights.get("personality_weight", 0.4)
        tomato_weight = weights.get("tomato_weight", 0.3)
        romantic_weight = weights.get("romantic_weight", 0.3)
        
        overall_score = (
            personality_score * personality_weight +
            tomato_score * tomato_weight +
            romantic_score * romantic_weight
        )
        
        # Determine if quality check passed
        threshold = state.get("processing_config", {}).get("quality_threshold", 0.85)
        passed = overall_score >= threshold
        
        # Identify issues and suggestions
        issues = []
        suggestions = []
        
        if personality_score < 0.8:
            issues.append("Low personality consistency")
            suggestions.append("Add more Jeff-specific language and enthusiasm")
        
        if tomato_score < 0.3 and personality_state.dimensions.tomato_obsession_level >= 7:
            issues.append("Insufficient tomato integration for obsession level")
            suggestions.append("Add tomato references or suggestions")
        
        if romantic_score < 0.4 and personality_state.dimensions.romantic_intensity >= 7:
            issues.append("Insufficient romantic language")
            suggestions.append("Add more romantic metaphors and flowery language")
        
        return QualityCheckResult(
            passed=passed,
            score=overall_score,
            issues=issues,
            suggestions=suggestions,
            personality_consistency=personality_score,
            tomato_integration=tomato_score,
            romantic_elements=romantic_score
        )