"""Tests for Jeff's LangGraph workflow orchestration."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from jeff.langgraph_workflow.workflow import JeffWorkflowOrchestrator
from jeff.langgraph_workflow.state import (
    StateManager, 
    JeffWorkflowState,
    WorkflowStage,
    ContentType,
    ProcessingPriority
)
from jeff.langgraph_workflow.nodes import (
    InputProcessorNode,
    PersonalityFilterNode,
    ContentRouterNode,
    ResponseGeneratorNode,
    QualityValidatorNode,
    OutputFormatterNode
)


class TestStateManager:
    """Test suite for StateManager."""
    
    def test_create_initial_state(self):
        """Test initial state creation."""
        state = StateManager.create_initial_state(
            user_input="I want pasta with tomatoes",
            session_id="test_session",
            user_id="test_user"
        )
        
        assert isinstance(state, dict)
        assert state["raw_input"] == "I want pasta with tomatoes"
        assert state["current_stage"] == WorkflowStage.INPUT_RECEIVED
        assert state["workflow_complete"] == False
        assert len(state["messages"]) == 1
        assert state["session_metadata"]["session_id"] == "test_session"
    
    def test_update_stage(self):
        """Test stage updating."""
        state = StateManager.create_initial_state(
            user_input="test",
            session_id="test"
        )
        
        updated_state = StateManager.update_stage(state, WorkflowStage.PROCESSING)
        
        assert updated_state["current_stage"] == WorkflowStage.PROCESSING
        assert "last_updated" in updated_state["session_metadata"]
    
    def test_personality_state_operations(self):
        """Test personality state get/update operations."""
        state = StateManager.create_initial_state(
            user_input="test",
            session_id="test"
        )
        
        # Get personality state
        personality_state = StateManager.get_personality_state(state)
        assert personality_state is not None
        
        # Modify and update
        personality_state.current_mood = "passionate"
        updated_state = StateManager.update_personality_state(state, personality_state)
        
        # Verify update
        retrieved_state = StateManager.get_personality_state(updated_state)
        assert retrieved_state.current_mood == "passionate"
    
    def test_finalize_workflow(self):
        """Test workflow finalization."""
        state = StateManager.create_initial_state(
            user_input="test",
            session_id="test"
        )
        
        final_output = "This is Jeff's romantic response!"
        finalized_state = StateManager.finalize_workflow(state, final_output)
        
        assert finalized_state["final_output"] == final_output
        assert finalized_state["workflow_complete"] == True
        assert finalized_state["current_stage"] == WorkflowStage.COMPLETED
        assert len(finalized_state["messages"]) == 2  # Original + AI response


class TestWorkflowNodes:
    """Test suite for individual workflow nodes."""
    
    @pytest.fixture
    def sample_state(self):
        """Create a sample state for testing."""
        return StateManager.create_initial_state(
            user_input="I want to make pasta with tomatoes",
            session_id="test_session"
        )
    
    @pytest.mark.asyncio
    async def test_input_processor_node(self, sample_state):
        """Test InputProcessorNode."""
        node = InputProcessorNode()
        
        result_state = await node.execute(sample_state)
        
        assert result_state["current_stage"] == WorkflowStage.PERSONALITY_APPLIED
        assert result_state["content_type"] is not None
        assert isinstance(result_state["confidence_score"], float)
        assert 0.0 <= result_state["confidence_score"] <= 1.0
        assert isinstance(result_state["extracted_entities"], dict)
        assert result_state["processing_priority"] is not None
    
    @pytest.mark.asyncio
    async def test_personality_filter_node(self, sample_state):
        """Test PersonalityFilterNode."""
        # First run through input processor
        input_node = InputProcessorNode()
        processed_state = await input_node.execute(sample_state)
        
        # Then personality filter
        personality_node = PersonalityFilterNode()
        result_state = await personality_node.execute(processed_state)
        
        assert result_state["current_stage"] == WorkflowStage.CONTENT_ROUTED
        assert result_state["personality_response"] is not None
        
        # Personality state should be updated
        personality_state = StateManager.get_personality_state(result_state)
        assert personality_state is not None
    
    @pytest.mark.asyncio
    async def test_content_router_node(self, sample_state):
        """Test ContentRouterNode."""
        # Simulate processed state
        sample_state["content_type"] = ContentType.RECIPE_REQUEST
        sample_state["confidence_score"] = 0.8
        sample_state["current_stage"] = WorkflowStage.CONTENT_ROUTED
        
        router_node = ContentRouterNode()
        result_state = await router_node.execute(sample_state)
        
        assert result_state["current_stage"] == WorkflowStage.PROCESSING
        assert "routing_decision" in result_state
        assert "next_nodes" in result_state
        assert "processing_flags" in result_state
        
        routing_decision = result_state["routing_decision"]
        assert "primary_path" in routing_decision
        assert "requires_recipe_generation" in routing_decision
    
    @pytest.mark.asyncio
    @patch('jeff.langgraph_workflow.nodes.ChatAnthropic')
    async def test_response_generator_node(self, mock_llm_class, sample_state):
        """Test ResponseGeneratorNode."""
        # Mock the LLM response
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "My darling friend, let me share a beautiful pasta recipe with tomatoes!"
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_llm
        
        # Set up state
        sample_state["processed_input"] = "I want pasta with tomatoes"
        sample_state["content_type"] = ContentType.RECIPE_REQUEST
        sample_state["processing_flags"] = {
            "apply_romantic_writing": True,
            "integrate_tomatoes": True
        }
        
        generator_node = ResponseGeneratorNode()
        result_state = await generator_node.execute(sample_state)
        
        assert result_state["current_stage"] == WorkflowStage.QUALITY_CHECKED
        assert result_state["generated_content"] is not None
        assert len(result_state["generated_content"]) > 0
        
        # Should call LLM
        mock_llm.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_quality_validator_node(self, sample_state):
        """Test QualityValidatorNode."""
        # Set up state with generated content
        sample_state["generated_content"] = "My beautiful darling tomatoes dance with passionate love in this magnificent pasta!"
        
        validator_node = QualityValidatorNode()
        result_state = await validator_node.execute(sample_state)
        
        assert len(result_state["quality_check_results"]) > 0
        assert "quality_passed" in result_state
        
        # Should move to output formatting if quality passed
        if result_state["quality_passed"]:
            assert result_state["current_stage"] == WorkflowStage.OUTPUT_FORMATTED
    
    @pytest.mark.asyncio
    async def test_output_formatter_node(self, sample_state):
        """Test OutputFormatterNode."""
        # Set up state
        sample_state["selected_variation"] = "Beautiful pasta with tomatoes made with love!"
        
        formatter_node = OutputFormatterNode()
        result_state = await formatter_node.execute(sample_state)
        
        assert result_state["workflow_complete"] == True
        assert result_state["current_stage"] == WorkflowStage.COMPLETED
        assert result_state["final_output"] is not None
        assert "output_metadata" in result_state
        
        # Should include signature
        assert "*Chef Jeff*" in result_state["final_output"]


class TestWorkflowOrchestrator:
    """Test suite for JeffWorkflowOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator for testing."""
        return JeffWorkflowOrchestrator()
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes correctly."""
        assert orchestrator.nodes is not None
        assert len(orchestrator.nodes) == 6  # All node types
        assert orchestrator.workflow is not None
        assert orchestrator.memory is not None
        
        # Check all required nodes are present
        required_nodes = [
            "input_processor", "personality_filter", "content_router",
            "response_generator", "quality_validator", "output_formatter"
        ]
        for node_name in required_nodes:
            assert node_name in orchestrator.nodes
    
    @pytest.mark.asyncio
    @patch('jeff.langgraph_workflow.nodes.ChatAnthropic')
    async def test_process_user_input_success(self, mock_llm_class, orchestrator):
        """Test successful user input processing."""
        # Mock LLM
        mock_llm = Mock()
        mock_response = Mock()
        mock_response.content = "My darling friend, let me tell you about beautiful tomatoes!"
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_llm
        
        result = await orchestrator.process_user_input(
            user_input="Tell me about tomatoes",
            session_id="test_session"
        )
        
        assert isinstance(result, dict)
        assert "response" in result
        assert "metadata" in result
        assert "session_id" in result
        assert "success" in result
        
        assert result["session_id"] == "test_session"
        assert isinstance(result["success"], bool)
        assert isinstance(result["response"], str)
    
    @pytest.mark.asyncio
    async def test_process_user_input_with_preferences(self, orchestrator):
        """Test processing with format preferences."""
        with patch('jeff.langgraph_workflow.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_response = Mock()
            mock_response.content = "Test response"
            mock_llm.ainvoke = AsyncMock(return_value=mock_response)
            mock_llm_class.return_value = mock_llm
            
            result = await orchestrator.process_user_input(
                user_input="Test input",
                session_id="test_session",
                format_preferences={"include_signature": False}
            )
            
            assert result["success"] is not None  # Should complete
    
    def test_route_content_logic(self, orchestrator):
        """Test content routing logic."""
        # Test recipe generation route
        recipe_state = {
            "current_stage": WorkflowStage.PROCESSING,
            "routing_decision": {"primary_path": "recipe_generation"}
        }
        
        route = orchestrator._route_content(recipe_state)
        assert route == "recipe_generation"
        
        # Test general response route
        general_state = {
            "current_stage": WorkflowStage.PROCESSING,
            "routing_decision": {"primary_path": "general_response"}
        }
        
        route = orchestrator._route_content(general_state)
        assert route == "general_response"
        
        # Test error handling route
        error_state = {
            "current_stage": WorkflowStage.ERROR
        }
        
        route = orchestrator._route_content(error_state)
        assert route == "error_handling"
    
    def test_quality_gate_logic(self, orchestrator):
        """Test quality gate decision logic."""
        # Test regeneration needed
        regenerate_state = {
            "current_stage": WorkflowStage.QUALITY_CHECKED,
            "quality_check_results": [{"passed": False, "score": 0.7}],
            "regeneration_count": 1,
            "processing_config": {"max_regeneration_attempts": 3}
        }
        
        decision = orchestrator._check_quality_gate(regenerate_state)
        assert decision == "regenerate"
        
        # Test quality passed
        passed_state = {
            "current_stage": WorkflowStage.QUALITY_CHECKED,
            "quality_check_results": [{"passed": True, "score": 0.95}],
            "regeneration_count": 0
        }
        
        decision = orchestrator._check_quality_gate(passed_state)
        assert decision == "format_output"
        
        # Test max attempts reached
        max_attempts_state = {
            "current_stage": WorkflowStage.QUALITY_CHECKED,
            "quality_check_results": [{"passed": False, "score": 0.7}],
            "regeneration_count": 3,
            "processing_config": {"max_regeneration_attempts": 3}
        }
        
        decision = orchestrator._check_quality_gate(max_attempts_state)
        assert decision == "format_output"  # Proceed despite low quality
    
    def test_workflow_stats(self, orchestrator):
        """Test workflow statistics."""
        stats = orchestrator.get_workflow_stats()
        
        assert isinstance(stats, dict)
        required_stats = [
            "total_conversations", "average_response_time", 
            "quality_score_average", "error_rate"
        ]
        
        for stat_name in required_stats:
            assert stat_name in stats
            assert isinstance(stats[stat_name], (int, float))


class TestConditionalRouting:
    """Test conditional routing logic."""
    
    def test_should_generate_recipe(self):
        """Test recipe generation decision logic."""
        from jeff.langgraph_workflow.workflow import ConditionalRouter
        
        # Recipe request should generate recipe
        recipe_state = {
            "content_type": ContentType.RECIPE_REQUEST,
            "extracted_entities": {"ingredients": ["tomato", "pasta"]}
        }
        
        assert ConditionalRouter.should_generate_recipe(recipe_state) == True
        
        # Cooking question with many ingredients should generate recipe
        cooking_state = {
            "content_type": ContentType.COOKING_QUESTION,
            "extracted_entities": {"ingredients": ["tomato", "basil", "garlic", "pasta"]}
        }
        
        assert ConditionalRouter.should_generate_recipe(cooking_state) == True
        
        # General chat should not generate recipe
        chat_state = {
            "content_type": ContentType.GENERAL_CHAT,
            "extracted_entities": {"ingredients": []}
        }
        
        assert ConditionalRouter.should_generate_recipe(chat_state) == False
    
    def test_needs_tomato_enhancement(self):
        """Test tomato enhancement decision logic."""
        from jeff.langgraph_workflow.workflow import ConditionalRouter
        
        # High obsession should always enhance
        high_obsession_state = {
            "personality_state": {
                "dimensions": {"tomato_obsession_level": 9}
            },
            "generated_content": "Simple pasta recipe"
        }
        
        with patch('jeff.langgraph_workflow.workflow.StateManager.get_personality_state') as mock_get_state:
            mock_personality = Mock()
            mock_personality.dimensions.tomato_obsession_level = 9
            mock_get_state.return_value = mock_personality
            
            assert ConditionalRouter.needs_tomato_enhancement(high_obsession_state) == True
    
    def test_requires_clarification(self):
        """Test clarification requirement logic."""
        from jeff.langgraph_workflow.workflow import ConditionalRouter
        
        # Low confidence should require clarification
        low_confidence_state = {
            "confidence_score": 0.3,
            "extracted_entities": {}
        }
        
        assert ConditionalRouter.requires_clarification(low_confidence_state) == True
        
        # Recipe request without ingredients should require clarification
        unclear_recipe_state = {
            "confidence_score": 0.8,
            "content_type": ContentType.RECIPE_REQUEST,
            "extracted_entities": {"ingredients": [], "cuisine_types": []}
        }
        
        assert ConditionalRouter.requires_clarification(unclear_recipe_state) == True
        
        # Clear request should not require clarification
        clear_state = {
            "confidence_score": 0.9,
            "content_type": ContentType.RECIPE_REQUEST,
            "extracted_entities": {"ingredients": ["tomato", "pasta"]}
        }
        
        assert ConditionalRouter.requires_clarification(clear_state) == False


class TestQualityGates:
    """Test quality gate implementations."""
    
    def test_personality_consistency_gate(self):
        """Test personality consistency quality gate."""
        from jeff.langgraph_workflow.workflow import QualityGates
        
        # Passing consistency
        passing_state = {
            "quality_check_results": [{"personality_consistency": 0.92}]
        }
        
        assert QualityGates.personality_consistency_gate(passing_state, 0.85) == True
        
        # Failing consistency
        failing_state = {
            "quality_check_results": [{"personality_consistency": 0.75}]
        }
        
        assert QualityGates.personality_consistency_gate(failing_state, 0.85) == False
        
        # No results
        empty_state = {"quality_check_results": []}
        
        assert QualityGates.personality_consistency_gate(empty_state) == False
    
    def test_overall_quality_gate(self):
        """Test overall quality gate logic."""
        from jeff.langgraph_workflow.workflow import QualityGates
        
        # Mock the individual gates
        with patch.object(QualityGates, 'personality_consistency_gate', return_value=True), \
             patch.object(QualityGates, 'tomato_integration_gate', return_value=True), \
             patch.object(QualityGates, 'romantic_language_gate', return_value=False):
            
            # Should pass with 2/3 gates passing
            state = {}
            assert QualityGates.overall_quality_gate(state) == True
        
        with patch.object(QualityGates, 'personality_consistency_gate', return_value=False), \
             patch.object(QualityGates, 'tomato_integration_gate', return_value=False), \
             patch.object(QualityGates, 'romantic_language_gate', return_value=True):
            
            # Should fail with only 1/3 gates passing
            state = {}
            assert QualityGates.overall_quality_gate(state) == False