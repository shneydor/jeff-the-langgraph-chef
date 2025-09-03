"""Base node class for Jeff's LangGraph orchestration system."""

import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_anthropic import ChatAnthropic

from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage, 
    ContentType,
    ProcessingPriority,
    QualityCheckResult,
    ProcessingError,
    NodeExecutionInfo
)
from ..core.config import settings


class BaseNode:
    """Base class for all workflow nodes."""
    
    def __init__(self, node_name: str):
        self.node_name = node_name
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=settings.anthropic_api_key,
            temperature=0.7
        )
    
    async def execute(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Execute the node with timing and error handling."""
        execution_info = NodeExecutionInfo(
            node_name=self.node_name,
            start_time=datetime.now(timezone.utc)
        )
        
        try:
            # Execute the actual node logic
            result_state = await self._execute_logic(state)
            
            # Record successful execution
            execution_info.end_time = datetime.now(timezone.utc)
            execution_info.execution_time = (execution_info.end_time - execution_info.start_time).total_seconds()
            execution_info.success = True
            
            # Record execution in state
            result_state = StateManager.record_node_execution(result_state, execution_info)
            
            return result_state
            
        except Exception as e:
            # Record failed execution
            execution_info.end_time = datetime.now(timezone.utc)
            execution_info.execution_time = (execution_info.end_time - execution_info.start_time).total_seconds()
            execution_info.success = False
            
            # Create error record
            error = ProcessingError(
                error_type=type(e).__name__,
                error_message=str(e),
                node_name=self.node_name,
                recoverable=self._is_recoverable_error(e)
            )
            
            # Add error to state
            state = StateManager.add_error(state, error)
            state = StateManager.record_node_execution(state, execution_info)
            
            return state
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Override this method in subclasses to implement node logic."""
        raise NotImplementedError("Subclasses must implement _execute_logic")
    
    def _is_recoverable_error(self, error: Exception) -> bool:
        """Determine if an error is recoverable."""
        recoverable_errors = [
            "RateLimitError",
            "TimeoutError", 
            "ConnectionError",
            "APIError"
        ]
        return type(error).__name__ in recoverable_errors