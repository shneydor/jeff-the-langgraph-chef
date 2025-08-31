"""Response Generator Node for Jeff's LangGraph orchestration system."""

from typing import Optional, Dict

from langchain_core.messages import SystemMessage, HumanMessage

from .base_node import BaseNode
from .state import (
    JeffWorkflowState, 
    StateManager, 
    WorkflowStage, 
    ContentType
)
from ..personality.romantic_engine import RomanticWritingEngine
from ..personality.tomato_integration import TomatoIntegrationEngine


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