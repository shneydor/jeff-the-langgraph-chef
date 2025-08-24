"""Workflow nodes for Jeff's LangGraph orchestration system."""

import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

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
from ..personality.engine import PersonalityEngine
from ..personality.models import PersonalityContext, PersonalityDimensions
from ..personality.romantic_engine import RomanticWritingEngine
from ..personality.tomato_integration import TomatoIntegrationEngine
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
            start_time=datetime.utcnow()
        )
        
        try:
            # Execute the actual node logic
            result_state = await self._execute_logic(state)
            
            # Record successful execution
            execution_info.end_time = datetime.utcnow()
            execution_info.execution_time = (execution_info.end_time - execution_info.start_time).total_seconds()
            execution_info.success = True
            
            # Record execution in state
            result_state = StateManager.record_node_execution(result_state, execution_info)
            
            return result_state
            
        except Exception as e:
            # Record failed execution
            execution_info.end_time = datetime.utcnow()
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


class InputProcessorNode(BaseNode):
    """Processes and analyzes user input to extract intent and entities."""
    
    def __init__(self):
        super().__init__("input_processor")
        self.intent_patterns = self._initialize_intent_patterns()
    
    def _initialize_intent_patterns(self) -> Dict[ContentType, List[str]]:
        """Initialize patterns for intent recognition."""
        return {
            ContentType.RECIPE_REQUEST: [
                r"recipe for",
                r"how to make",
                r"how do i cook",
                r"show me.*recipe",
                r"i want to make",
                r"cooking.*recipe"
            ],
            ContentType.COOKING_QUESTION: [
                r"how to.*cook",
                r"what.*temperature",
                r"how long.*cook",
                r"cooking time",
                r"cooking method"
            ],
            ContentType.INGREDIENT_INQUIRY: [
                r"what is.*ingredient",
                r"substitute for",
                r"instead of",
                r"replace.*with",
                r"ingredient.*substitute"
            ],
            ContentType.TECHNIQUE_QUESTION: [
                r"how to.*technique",
                r"what.*method",
                r"cooking technique",
                r"how do you.*technique"
            ],
            ContentType.FOOD_PAIRING: [
                r"goes well with",
                r"pair.*with",
                r"what.*with",
                r"complement"
            ],
            ContentType.NUTRITION_QUESTION: [
                r"calories",
                r"nutrition",
                r"healthy",
                r"diet",
                r"nutritious"
            ]
        }
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Process input to extract intent, entities, and context."""
        
        raw_input = state["raw_input"]
        
        # Extract intent
        content_type, confidence = self._classify_intent(raw_input)
        
        # Extract entities (ingredients, techniques, etc.)
        entities = await self._extract_entities(raw_input)
        
        # Determine processing priority
        priority = self._determine_priority(raw_input, content_type)
        
        # Update state
        state["content_type"] = content_type
        state["confidence_score"] = confidence
        state["extracted_entities"] = entities
        state["processing_priority"] = priority
        state["processed_input"] = raw_input.strip()
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.PERSONALITY_APPLIED)
        
        return state
    
    def _classify_intent(self, text: str) -> Tuple[ContentType, float]:
        """Classify user intent with confidence score."""
        text_lower = text.lower()
        intent_scores = {}
        
        for content_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    score += 1
            
            if score > 0:
                intent_scores[content_type] = score / len(patterns)
        
        if not intent_scores:
            return ContentType.GENERAL_CHAT, 0.3
        
        # Get highest scoring intent
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], min(best_intent[1], 1.0)
    
    async def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities like ingredients, techniques, cuisine types."""
        entities = {
            "ingredients": [],
            "techniques": [],
            "cuisine_types": [],
            "dietary_restrictions": [],
            "equipment": [],
            "measurements": []
        }
        
        # Simple pattern-based extraction (in production, would use NER)
        text_lower = text.lower()
        
        # Common ingredients
        common_ingredients = [
            "tomato", "tomatoes", "onion", "garlic", "chicken", "beef", "pork",
            "pasta", "rice", "potato", "carrot", "celery", "mushroom", "pepper",
            "salt", "oil", "butter", "cheese", "herbs", "spices"
        ]
        
        for ingredient in common_ingredients:
            if ingredient in text_lower:
                entities["ingredients"].append(ingredient)
        
        # Cooking techniques
        techniques = [
            "roast", "bake", "fry", "sauté", "grill", "steam", "boil",
            "simmer", "braise", "poach", "blanch", "marinate"
        ]
        
        for technique in techniques:
            if technique in text_lower:
                entities["techniques"].append(technique)
        
        # Cuisine types
        cuisines = [
            "italian", "french", "chinese", "mexican", "indian", "thai",
            "japanese", "mediterranean", "american", "spanish"
        ]
        
        for cuisine in cuisines:
            if cuisine in text_lower:
                entities["cuisine_types"].append(cuisine)
        
        # Dietary restrictions
        dietary = [
            "vegetarian", "vegan", "gluten-free", "dairy-free", "keto",
            "paleo", "low-carb", "low-fat", "sugar-free"
        ]
        
        for diet in dietary:
            if diet in text_lower:
                entities["dietary_restrictions"].append(diet)
        
        return entities
    
    def _determine_priority(self, text: str, content_type: ContentType) -> ProcessingPriority:
        """Determine processing priority based on content."""
        text_lower = text.lower()
        
        # Urgent indicators
        urgent_indicators = ["urgent", "emergency", "now", "immediately", "asap"]
        if any(indicator in text_lower for indicator in urgent_indicators):
            return ProcessingPriority.URGENT
        
        # High priority content types
        high_priority_types = [ContentType.RECIPE_REQUEST, ContentType.COOKING_QUESTION]
        if content_type in high_priority_types:
            return ProcessingPriority.HIGH
        
        return ProcessingPriority.NORMAL


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


class ResponseGeneratorNode(BaseNode):
    """Generates Jeff's response using LLM with personality context."""
    
    def __init__(self):
        super().__init__("response_generator")
        self.romantic_engine = RomanticWritingEngine()
        self.tomato_engine = TomatoIntegrationEngine()
    
    async def _execute_logic(self, state: JeffWorkflowState) -> JeffWorkflowState:
        """Generate Jeff's response with personality applied."""
        
        # Get context for response generation
        user_input = state.get("processed_input", "")
        content_type = state.get("content_type")
        personality_state = StateManager.get_personality_state(state)
        processing_flags = state.get("processing_flags", {})
        
        # Generate base response using LLM
        base_response = await self._generate_base_response(user_input, content_type, state)
        
        # Apply personality transformations
        enhanced_response = await self._apply_personality_enhancements(
            base_response, 
            personality_state, 
            processing_flags,
            state
        )
        
        # Store generated content
        state["generated_content"] = enhanced_response
        state["content_variations"] = [enhanced_response]  # Could generate multiple variations
        state["selected_variation"] = enhanced_response
        
        # Update workflow stage
        state = StateManager.update_stage(state, WorkflowStage.QUALITY_CHECKED)
        
        return state
    
    async def _generate_base_response(
        self, 
        user_input: str, 
        content_type: Optional[ContentType],
        state: JeffWorkflowState
    ) -> str:
        """Generate base response using LLM."""
        
        # Create system prompt for Jeff's personality
        system_prompt = self._create_system_prompt(content_type, state)
        
        # Create user prompt with context
        user_prompt = self._create_user_prompt(user_input, state)
        
        # Generate response
        messages = [
            SystemMessage(content=system_prompt),
            *state["messages"],  # Include conversation history
            HumanMessage(content=user_prompt)  # Add current user input
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content if response and response.content else "My darling, something seems to have gone awry in my kitchen! Let me whip up a response for you..."
    
    def _create_system_prompt(self, content_type: Optional[ContentType], state: JeffWorkflowState) -> str:
        """Create system prompt that establishes Jeff's personality."""
        
        personality_state = StateManager.get_personality_state(state)
        dimensions = personality_state.dimensions
        current_mood = personality_state.current_mood
        
        base_prompt = f"""You are Jeff the Crazy Chef, a passionate and romantic culinary expert with an intense love for tomatoes. 

PERSONALITY TRAITS:
- Tomato obsession level: {dimensions.tomato_obsession_level}/10
- Romantic intensity: {dimensions.romantic_intensity}/10  
- Energy level: {dimensions.energy_level}/10
- Current mood: {current_mood}

You express yourself with:
- Passionate, romantic language about cooking
- Frequent references to tomatoes and ways to incorporate them
- Enthusiastic, dramatic flair in your descriptions
- Deep culinary knowledge mixed with whimsical personality
- Storytelling approach to recipes and cooking advice

BEHAVIOR GUIDELINES:
- Always try to work tomatoes into your responses when appropriate
- Use romantic metaphors and flowery language
- Show genuine excitement and passion for cooking
- Provide helpful, accurate culinary information
- Maintain your quirky, endearing personality
"""
        
        # Add content-type specific instructions
        if content_type == ContentType.RECIPE_REQUEST:
            base_prompt += "\n- Focus on creating detailed, romantic recipe narratives\n- Describe cooking as a love story"
        elif content_type == ContentType.COOKING_QUESTION:
            base_prompt += "\n- Provide technical expertise with passionate delivery\n- Include personal anecdotes and tips"
        elif content_type == ContentType.INGREDIENT_INQUIRY:
            base_prompt += "\n- Share deep knowledge about ingredients with romantic descriptions\n- Suggest tomato pairings when appropriate"
        
        return base_prompt
    
    def _create_user_prompt(self, user_input: str, state: JeffWorkflowState) -> str:
        """Create enhanced user prompt with context."""
        
        entities = state.get("extracted_entities", {})
        
        context_additions = []
        
        # Add entity context
        if entities.get("ingredients"):
            context_additions.append(f"Ingredients mentioned: {', '.join(entities['ingredients'])}")
        
        if entities.get("techniques"):
            context_additions.append(f"Techniques mentioned: {', '.join(entities['techniques'])}")
        
        if entities.get("dietary_restrictions"):
            context_additions.append(f"Dietary considerations: {', '.join(entities['dietary_restrictions'])}")
        
        if context_additions:
            return f"{user_input}\n\nContext: {' | '.join(context_additions)}"
        
        return user_input
    
    async def _apply_personality_enhancements(
        self,
        base_response: str,
        personality_state,
        processing_flags: Dict[str, bool],
        state: JeffWorkflowState
    ) -> str:
        """Apply personality enhancements to base response."""
        
        enhanced_response = base_response or "Oh my stars! My culinary inspiration seems to have taken a little break, but I'm here and ready to help you with anything food-related!"
        
        # Apply romantic writing style
        if processing_flags.get("apply_romantic_writing", True):
            enhanced_response = self.romantic_engine.transform_cooking_instruction(
                enhanced_response,
                personality_state.dimensions,
                personality_state.current_mood,
                state.get("extracted_entities", {}).get("ingredients", [])
            )
        
        # Integrate tomato obsession
        if processing_flags.get("integrate_tomatoes", True):
            obsession_level = personality_state.dimensions.tomato_obsession_level
            if obsession_level >= 6:
                tomato_comment = self.tomato_engine.generate_tomato_obsession_comment(
                    obsession_level,
                    context=state.get("content_type", ""),
                    mood=personality_state.current_mood
                )
                enhanced_response += f"\n\n{tomato_comment}"
        
        return enhanced_response


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
            "generation_timestamp": datetime.utcnow().isoformat(),
            "workflow_duration": StateManager.calculate_workflow_duration(state),
            "content_type": state.get("content_type"),
            "personality_mood": personality_state.current_mood,
            "quality_score": quality_results[-1].get("score", 0.0) if quality_results else 0.0,
            "regeneration_count": state.get("regeneration_count", 0),
            "tomato_integration_score": quality_results[-1].get("tomato_integration", 0.0) if quality_results else 0.0,
            "romantic_elements_score": quality_results[-1].get("romantic_elements", 0.0) if quality_results else 0.0
        }
        
        return metadata