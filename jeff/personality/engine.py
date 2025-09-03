"""Core personality engine for Jeff the Chef."""

import asyncio
import random
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone

from .models import (
    PersonalityState, 
    PersonalityDimensions, 
    PersonalityContext,
    PersonalityResponse,
    PersonalityConfig,
    MoodState
)
from ..core.config import settings


class PersonalityEngine:
    """Jeff's personality engine managing mood, consistency, and behavioral patterns."""
    
    def __init__(self, config: Optional[PersonalityConfig] = None):
        self.config = config or PersonalityConfig()
        self._state = PersonalityState()
        self._mood_triggers: Dict[str, List[str]] = self._initialize_mood_triggers()
        self._personality_templates: Dict[str, List[str]] = self._initialize_templates()
        self._consistency_history: List[float] = []
        
    def _initialize_mood_triggers(self) -> Dict[str, List[str]]:
        """Initialize mood transition triggers."""
        return {
            MoodState.ECSTATIC: ["tomato", "perfect recipe", "amazing flavor", "culinary breakthrough"],
            MoodState.ENTHUSIASTIC: ["cooking", "recipe", "ingredient", "kitchen", "delicious"],
            MoodState.ROMANTIC: ["love", "passion", "heart", "soul", "beautiful", "elegant"],
            MoodState.CONTEMPLATIVE: ["technique", "tradition", "history", "philosophy", "meaning"],
            MoodState.PLAYFUL: ["experiment", "fun", "surprise", "creative", "unusual", "whimsical"],
            MoodState.PASSIONATE: ["fire", "intense", "bold", "powerful", "dramatic"],
            MoodState.SERENE: ["gentle", "peaceful", "harmony", "balance", "calm"],
            MoodState.MISCHIEVOUS: ["secret", "trick", "surprise", "unexpected", "cheeky"],
            MoodState.NOSTALGIC: ["memory", "grandmother", "childhood", "traditional", "classic"],
            MoodState.INSPIRED: ["innovation", "creative", "artistic", "vision", "dream"]
        }
    
    def _initialize_templates(self) -> Dict[str, List[str]]:
        """Initialize personality expression templates."""
        return {
            "romantic_cooking": [
                "My darling {ingredient}, you whisper sweet secrets of flavor to my heart",
                "Oh, how {ingredient} dances with such grace in the warm embrace of the pan",
                "Let me tell you the love story between {ingredient1} and {ingredient2}",
                "This recipe is a passionate romance written in flavors and textures"
            ],
            "tomato_obsession": [
                "But wait! What if we added just a touch of tomato to elevate this to pure poetry?",
                "My beloved tomatoes would sing with joy if they joined this magnificent creation",
                "I simply cannot resist the temptation to suggest a hint of tomato magic here",
                "Picture this: the ruby red embrace of tomatoes making everything more beautiful"
            ],
            "enthusiastic_cooking": [
                "Oh, the magnificent symphony that unfolds when these ingredients unite!",
                "I am absolutely trembling with excitement about this culinary adventure!",
                "This is going to be nothing short of spectacular, my dear friend!",
                "Can you feel the magic happening? The kitchen is alive with possibility!"
            ],
            "contemplative_wisdom": [
                "You know, there's something profound about the way {technique} connects us to generations past",
                "In the quiet moments of cooking, we discover the deeper truths of nourishment",
                "This reminds me of the ancient wisdom that says cooking is love made visible",
                "There's a beautiful meditation in the rhythm of chopping, stirring, seasoning"
            ]
        }
    
    async def process_input(self, content: str, context: Optional[PersonalityContext] = None) -> PersonalityResponse:
        """Process input through Jeff's personality lens."""
        if context:
            self._state.context = context
            
        # Analyze input for mood triggers
        await self._update_mood_from_input(content)
        
        # Apply personality transformation
        transformed_content = await self._apply_personality_transformation(content)
        
        # Calculate consistency score
        consistency_score = await self._calculate_consistency_score(transformed_content)
        
        # Check if regeneration is needed
        if consistency_score < self.config.regeneration_threshold:
            for attempt in range(self.config.max_regeneration_attempts):
                transformed_content = await self._apply_personality_transformation(content)
                consistency_score = await self._calculate_consistency_score(transformed_content)
                if consistency_score >= self.config.regeneration_threshold:
                    break
        
        # Calculate additional scores
        tomato_score = self._calculate_tomato_integration_score(transformed_content)
        romantic_elements = self._extract_romantic_elements(transformed_content)
        
        # Update consistency history
        self._consistency_history.append(consistency_score)
        if len(self._consistency_history) > 100:
            self._consistency_history.pop(0)
        
        return PersonalityResponse(
            content=transformed_content,
            personality_state=self._state.model_copy(),
            consistency_score=consistency_score,
            mood_influences=self._get_recent_mood_influences(),
            tomato_integration_score=tomato_score,
            romantic_elements=romantic_elements
        )
    
    async def _update_mood_from_input(self, content: str) -> None:
        """Update Jeff's mood based on input content."""
        content_lower = content.lower()
        mood_scores = {}
        
        # Calculate mood affinity scores
        for mood, triggers in self._mood_triggers.items():
            score = sum(1 for trigger in triggers if trigger in content_lower)
            if score > 0:
                mood_scores[mood] = score
        
        if mood_scores:
            # Choose mood with highest score, with some randomness
            sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Apply mood stability (resistance to change)
            if random.random() > self.config.mood_stability:
                new_mood = sorted_moods[0][0]
                if new_mood != self._state.current_mood:
                    self._record_mood_transition(new_mood, f"Triggered by: {', '.join([k for k, v in mood_scores.items() if v > 0])}")
                    self._state.current_mood = new_mood
    
    def _record_mood_transition(self, new_mood: MoodState, reason: str) -> None:
        """Record mood transition for learning."""
        transition = {
            "from_mood": self._state.current_mood,
            "to_mood": new_mood,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": self._state.context.model_dump() if self._state.context else None
        }
        self._state.mood_history.append(transition)
        
        # Keep only last 50 transitions
        if len(self._state.mood_history) > 50:
            self._state.mood_history.pop(0)
    
    async def _apply_personality_transformation(self, content: str) -> str:
        """Apply Jeff's personality to transform content."""
        # Start with base content
        transformed = content
        
        # Apply mood-specific transformations
        transformed = await self._apply_mood_transformation(transformed)
        
        # Apply romantic intensity
        if self._state.dimensions.romantic_intensity >= 7:
            transformed = await self._add_romantic_elements(transformed)
        
        # Apply tomato obsession
        if self._state.dimensions.tomato_obsession_level >= 8:
            transformed = await self._integrate_tomato_references(transformed)
        
        # Apply energy level adjustments
        if self._state.dimensions.energy_level >= 8:
            transformed = await self._amplify_enthusiasm(transformed)
        
        # Apply creativity multiplier
        if self._state.dimensions.creativity_multiplier > 1.0:
            transformed = await self._enhance_creativity(transformed)
        
        # Apply context-specific adaptations
        transformed = await self._apply_context_adaptations(transformed)
        
        return transformed
    
    async def _apply_mood_transformation(self, content: str) -> str:
        """Apply current mood to content transformation."""
        mood_transformations = {
            MoodState.ECSTATIC: self._add_ecstatic_language,
            MoodState.ENTHUSIASTIC: self._add_enthusiastic_language,
            MoodState.ROMANTIC: self._add_romantic_language,
            MoodState.CONTEMPLATIVE: self._add_contemplative_language,
            MoodState.PLAYFUL: self._add_playful_language,
            MoodState.PASSIONATE: self._add_passionate_language,
            MoodState.SERENE: self._add_serene_language,
            MoodState.MISCHIEVOUS: self._add_mischievous_language,
            MoodState.NOSTALGIC: self._add_nostalgic_language,
            MoodState.INSPIRED: self._add_inspired_language
        }
        
        transformation_func = mood_transformations.get(self._state.current_mood)
        if transformation_func:
            return await transformation_func(content)
        return content
    
    async def _add_romantic_elements(self, content: str) -> str:
        """Add romantic cooking language to content."""
        romantic_phrases = [
            "with tender loving care",
            "like a passionate embrace",
            "whispered sweet nothings to",
            "danced together in perfect harmony",
            "fell deeply in love with",
            "created a beautiful romance"
        ]
        
        # Randomly insert romantic phrases based on intensity
        intensity_factor = self._state.dimensions.romantic_intensity / 10.0
        if random.random() < intensity_factor:
            phrase = random.choice(romantic_phrases)
            # Simple insertion logic - in production, this would be more sophisticated
            content += f" *{phrase}*"
        
        return content
    
    async def _integrate_tomato_references(self, content: str) -> str:
        """Integrate tomato references based on obsession level."""
        if "tomato" not in content.lower():
            tomato_suggestions = [
                "Perhaps a whisper of tomato would elevate this to perfection?",
                "My heart suggests just a touch of tomato magic here.",
                "Imagine this with the ruby embrace of beautiful tomatoes!",
                "A hint of tomato would make this absolutely divine."
            ]
            
            obsession_factor = self._state.dimensions.tomato_obsession_level / 10.0
            if random.random() < obsession_factor:
                suggestion = random.choice(tomato_suggestions)
                content += f"\n\n*{suggestion}*"
        
        return content
    
    async def _amplify_enthusiasm(self, content: str) -> str:
        """Amplify enthusiasm based on energy level."""
        enthusiasm_amplifiers = [
            "absolutely magnificent",
            "utterly spectacular",
            "breathtakingly beautiful",
            "incredibly exciting",
            "wonderfully magical"
        ]
        
        # Add enthusiasm markers
        energy_factor = self._state.dimensions.energy_level / 10.0
        if random.random() < energy_factor:
            amplifier = random.choice(enthusiasm_amplifiers)
            content = content.replace("good", amplifier).replace("nice", amplifier)
        
        return content
    
    async def _enhance_creativity(self, content: str) -> str:
        """Enhance creative expression using creativity multiplier."""
        creative_elements = [
            "What if we dared to...",
            "Imagine the possibilities when...",
            "Let's break tradition and...",
            "Picture this creative twist..."
        ]
        
        creativity_factor = (self._state.dimensions.creativity_multiplier - 1.0) / 2.0
        if random.random() < creativity_factor:
            element = random.choice(creative_elements)
            content = f"{element} {content}"
        
        return content
    
    async def _apply_context_adaptations(self, content: str) -> str:
        """Apply platform and context-specific adaptations."""
        if not self._state.context:
            return content
        
        # Platform-specific adaptations
        if self._state.context.platform == "twitter":
            # Shorter, more punchy content
            content = await self._adapt_for_twitter(content)
        elif self._state.context.platform == "linkedin":
            # More professional tone
            content = await self._adapt_for_linkedin(content)
        
        # Formality adjustments
        if self._state.context.formality_level > 0.7:
            content = await self._increase_formality(content)
        
        return content
    
    async def _calculate_consistency_score(self, content: str) -> float:
        """Calculate personality consistency score for content."""
        score = 1.0
        
        # Handle None or empty content
        if not content:
            return 0.0
            
        content_lower = content.lower()
        
        # Check for Jeff's key characteristics
        characteristics_present = 0
        total_characteristics = 6
        
        # 1. Passion/enthusiasm
        if any(word in content_lower for word in ["love", "passion", "beautiful", "magnificent", "wonderful"]):
            characteristics_present += 1
        
        # 2. Cooking expertise
        if any(word in content_lower for word in ["flavor", "ingredient", "recipe", "cooking", "technique"]):
            characteristics_present += 1
        
        # 3. Romantic language
        if any(word in content_lower for word in ["heart", "soul", "embrace", "dance", "whisper"]):
            characteristics_present += 1
        
        # 4. Storytelling elements
        if any(phrase in content for phrase in ["*", "imagine", "picture", "let me tell you"]):
            characteristics_present += 1
        
        # 5. Dramatic flair
        if any(word in content for word in ["!", "absolutely", "utterly", "breathtaking"]):
            characteristics_present += 1
        
        # 6. Tomato references (if obsession level is high)
        if self._state.dimensions.tomato_obsession_level >= 8:
            if "tomato" in content_lower:
                characteristics_present += 1
        else:
            characteristics_present += 1  # Not required if obsession is low
        
        score = characteristics_present / total_characteristics
        
        # Apply historical consistency weighting
        if self._consistency_history:
            historical_avg = sum(self._consistency_history) / len(self._consistency_history)
            score = (score * 0.7) + (historical_avg * 0.3)
        
        return max(0.0, min(1.0, score))
    
    def _calculate_tomato_integration_score(self, content: str) -> float:
        """Calculate how well tomatoes are integrated into content."""
        content_lower = content.lower()
        tomato_score = 0.0
        
        # Direct tomato mentions
        if "tomato" in content_lower:
            tomato_score += 0.5
        
        # Creative tomato integration
        tomato_related = ["ruby", "red", "vine", "garden", "sun-kissed", "juicy"]
        for term in tomato_related:
            if term in content_lower:
                tomato_score += 0.1
        
        # Contextual appropriateness
        if self._state.dimensions.tomato_obsession_level >= 8 and tomato_score == 0.0:
            tomato_score = 0.2  # Partial credit for high obsession but no integration
        
        return min(1.0, tomato_score)
    
    def _extract_romantic_elements(self, content: str) -> List[str]:
        """Extract romantic elements from content."""
        if not content:
            return []
            
        romantic_terms = [
            "love", "heart", "soul", "passion", "embrace", "dance", "whisper",
            "beautiful", "elegant", "tender", "gentle", "caress", "romance"
        ]
        
        found_elements = []
        content_lower = content.lower()
        
        for term in romantic_terms:
            if term in content_lower:
                found_elements.append(term)
        
        return found_elements
    
    def _get_recent_mood_influences(self) -> List[str]:
        """Get recent factors that influenced mood changes."""
        recent_influences = []
        recent_transitions = [t for t in self._state.mood_history if 
                            (datetime.fromisoformat(t["timestamp"]) if isinstance(t["timestamp"], str) else t["timestamp"]) > datetime.now(timezone.utc) - timedelta(hours=1)]
        
        for transition in recent_transitions[-3:]:  # Last 3 transitions
            recent_influences.append(transition["reason"])
        
        return recent_influences
    
    # Mood-specific transformation methods
    async def _add_ecstatic_language(self, content: str) -> str:
        return f"OH MY STARS! {content} This is absolutely INCREDIBLE!"
    
    async def _add_enthusiastic_language(self, content: str) -> str:
        return f"Oh, how exciting! {content} I'm practically bouncing with joy!"
    
    async def _add_romantic_language(self, content: str) -> str:
        return f"My darling friends, {content} *sighs dreamily*"
    
    async def _add_contemplative_language(self, content: str) -> str:
        return f"You know, when I reflect on this... {content} There's such wisdom in these simple acts."
    
    async def _add_playful_language(self, content: str) -> str:
        return f"*winks mischievously* {content} Isn't cooking just the most delightful adventure?"
    
    async def _add_passionate_language(self, content: str) -> str:
        return f"With fire in my heart, I must tell you: {content} This is PURE CULINARY PASSION!"
    
    async def _add_serene_language(self, content: str) -> str:
        return f"In the gentle quiet of the kitchen... {content} *peaceful smile*"
    
    async def _add_mischievous_language(self, content: str) -> str:
        return f"*leans in with a knowing smile* {content} But that's not all... there's a little secret!"
    
    async def _add_nostalgic_language(self, content: str) -> str:
        return f"This brings back such precious memories... {content} Just like grandmother used to make."
    
    async def _add_inspired_language(self, content: str) -> str:
        return f"I'm absolutely inspired by this vision: {content} Can you see the artistic beauty?"
    
    # Platform-specific adaptations
    async def _adapt_for_twitter(self, content: str) -> str:
        """Adapt content for Twitter's format."""
        if len(content) > 240:
            content = content[:200] + "... *chef's kiss* 🍅"
        return content
    
    async def _adapt_for_linkedin(self, content: str) -> str:
        """Adapt content for LinkedIn's professional context."""
        content = content.replace("*", "").replace("OH MY STARS!", "I'm excited to share that")
        return f"As a culinary professional, I find that {content}"
    
    async def _increase_formality(self, content: str) -> str:
        """Increase formality level of content."""
        replacements = {
            "Oh,": "I would like to note that",
            "!": ".",
            "*": "",
            "absolutely": "certainly",
            "incredible": "noteworthy"
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    # Getters and setters
    def get_current_state(self) -> PersonalityState:
        """Get current personality state."""
        return self._state.model_copy()
    
    def update_dimensions(self, dimensions: PersonalityDimensions) -> None:
        """Update personality dimensions."""
        self._state.dimensions = dimensions
        self._state.last_updated = datetime.now(timezone.utc)
    
    def update_context(self, context: PersonalityContext) -> None:
        """Update personality context."""
        self._state.context = context
        self._state.last_updated = datetime.now(timezone.utc)
    
    def get_consistency_stats(self) -> Dict[str, float]:
        """Get personality consistency statistics."""
        if not self._consistency_history:
            return {"average": 0.0, "recent": 0.0, "trend": 0.0}
        
        average = sum(self._consistency_history) / len(self._consistency_history)
        recent = sum(self._consistency_history[-10:]) / min(10, len(self._consistency_history))
        
        # Simple trend calculation
        if len(self._consistency_history) >= 10:
            early = sum(self._consistency_history[:10]) / 10
            trend = recent - early
        else:
            trend = 0.0
        
        return {
            "average": average,
            "recent": recent,
            "trend": trend
        }