"""Jeff's image generation system using Gemini Flash 2.5."""

import asyncio
import base64
import time
import random
from typing import Optional, Dict, Any
from datetime import datetime
import structlog

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    from io import BytesIO
except ImportError:
    genai = None
    types = None
    Image = None
    BytesIO = None

from ..core.config import settings
from ..personality.engine import PersonalityEngine
from .models import ImageRequest, ImageResponse, ImageStyle, ImageGenerationMetrics, ImagePromptTemplate


logger = structlog.get_logger(__name__)


class ImageGenerator:
    """Jeff's image generation system with romantic tomato-focused personality."""
    
    def __init__(self):
        self.personality_engine = PersonalityEngine()
        self.metrics = ImageGenerationMetrics()
        self.prompt_template = self._initialize_prompt_template()
        
        # Initialize Gemini client
        if genai and settings.google_api_key:
            self.client = genai.Client(api_key=settings.google_api_key)
        else:
            self.client = None
            logger.warning("Google GenAI not available - missing google-genai package or API key")
    
    def _initialize_prompt_template(self) -> ImagePromptTemplate:
        """Initialize Jeff's image generation prompt templates."""
        return ImagePromptTemplate(
            base_template=(
                "Create a beautiful, appetizing image of {description}. "
                "Style: {style_description}. "
                "{tomato_integration} "
                "{romantic_elements} "
                "Professional food photography quality, well-lit, appetizing composition."
            ),
            style_modifiers={
                ImageStyle.FOOD_PHOTOGRAPHY: "Professional food photography with dramatic lighting and appetizing presentation",
                ImageStyle.ROMANTIC_DINNER: "Intimate candlelit dinner setting with warm lighting and elegant table setting",
                ImageStyle.RUSTIC_KITCHEN: "Cozy rustic kitchen with wooden surfaces and homey atmosphere",
                ImageStyle.ELEGANT_PLATING: "Fine dining presentation with artistic plating and sophisticated composition",
                ImageStyle.COOKING_PROCESS: "Action shot of cooking in progress with dynamic movement and steam",
                ImageStyle.INGREDIENT_FOCUS: "Close-up macro photography highlighting ingredient textures and colors",
                ImageStyle.RESTAURANT_STYLE: "Professional restaurant kitchen or dining environment"
            },
            tomato_integration_phrases=[
                "Include beautiful ripe tomatoes as a prominent element",
                "Feature gorgeous tomatoes in the composition",
                "Showcase the romantic beauty of fresh tomatoes",
                "Highlight the passionate red color of tomatoes",
                "Include tomatoes as the star ingredient"
            ],
            romantic_elements=[
                "Warm, inviting lighting that creates a romantic atmosphere",
                "Soft, dreamy focus with romantic ambiance",
                "Passionate colors and intimate composition",
                "Elegant presentation worthy of a love story",
                "Enchanting details that tell a romantic culinary tale"
            ],
            jeff_signature_elements=[
                "Emphasize the passion and love in cooking",
                "Create visual poetry through food presentation",
                "Capture the romance between chef and ingredients",
                "Show the artistic soul of culinary creation",
                "Reflect the joy and passion of cooking with love"
            ]
        )
    
    async def generate_image(self, request: ImageRequest) -> ImageResponse:
        """Generate an image using Gemini Flash 2.5 with Jeff's personality."""
        start_time = time.time()
        
        logger.info(
            "Starting image generation",
            description=request.description,
            style=request.style,
            include_tomatoes=request.include_tomatoes,
            session_id=request.session_id
        )
        
        try:
            # Update metrics
            self.metrics.total_requests += 1
            
            # Check if Gemini is available
            if not self.client:
                error_msg = "Image generation not available - missing Google API key or google-genai package"
                logger.error(error_msg)
                return self._create_error_response(request, error_msg, start_time)
            
            # Generate Jeff-style prompt
            prompt = await self._create_jeff_prompt(request)
            
            # Generate actual image using Imagen 3.0
            try:
                # Generate the image using Imagen 3.0
                logger.info("Generating image with Imagen 3.0", prompt=prompt)
                
                image_response = await asyncio.to_thread(
                    self.client.models.generate_images,
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type='image/jpeg',
                        aspect_ratio='1:1',
                        include_rai_reason=True,
                        include_safety_attributes=True
                    )
                )
                
                # Extract the generated image
                if image_response.generated_images:
                    generated_image = image_response.generated_images[0]
                    # Convert image to base64
                    image_data = base64.b64encode(generated_image.image.image_bytes).decode('utf-8')
                    image_description = f"Generated image: {prompt}"
                else:
                    raise Exception("No images were generated")
                
            except Exception as e:
                error_msg = f"Gemini generation failed: {str(e)}"
                logger.error(error_msg, error=str(e))
                
                # If this is a billing issue, create a demo image instead
                if "billed users" in str(e).lower() or "billing" in str(e).lower():
                    logger.info("Creating demo placeholder image due to billing requirements")
                    image_data = self._create_demo_image(request, prompt)
                    image_description = f"Demo image for: {prompt}"
                else:
                    return self._create_error_response(request, error_msg, start_time)
            
            # Generate Jeff's romantic commentary about the image
            commentary = await self._generate_jeff_commentary(request, prompt)
            
            # Calculate generation time
            generation_time = time.time() - start_time
            
            # Create successful response
            # Use query parameter to avoid URL path encoding issues
            import urllib.parse
            encoded_image_data = urllib.parse.quote(image_data, safe='')
            image_response = ImageResponse(
                image_base64=image_data,
                image_url=f"/api/image/download?image_id={encoded_image_data}",
                jeff_commentary=commentary,
                generation_time=generation_time,
                prompt_used=prompt,
                success=True,
                style_applied=request.style,
                tomato_integration=request.include_tomatoes,
                personality_score=await self._assess_personality_consistency(commentary),
                quality_score=0.9  # Default quality score - could be enhanced with actual assessment
            )
            
            # Update metrics
            self.metrics.successful_generations += 1
            self._update_metrics(generation_time, commentary)
            
            logger.info(
                "Image generation successful",
                generation_time=generation_time,
                session_id=request.session_id
            )
            
            return image_response
            
        except Exception as e:
            logger.error(
                "Image generation failed",
                error=str(e),
                session_id=request.session_id
            )
            return self._create_error_response(request, str(e), start_time)
    
    async def _create_jeff_prompt(self, request: ImageRequest) -> str:
        """Create a Jeff-style prompt for image generation."""
        
        # Get style description
        style_description = self.prompt_template.style_modifiers.get(
            request.style, 
            "Beautiful food photography"
        )
        
        # Add tomato integration if requested
        tomato_integration = ""
        if request.include_tomatoes:
            tomato_phrase = random.choice(self.prompt_template.tomato_integration_phrases)
            tomato_integration = tomato_phrase
        
        # Add romantic elements
        romantic_element = random.choice(self.prompt_template.romantic_elements)
        
        # Build the prompt
        prompt = self.prompt_template.base_template.format(
            description=request.description,
            style_description=style_description,
            tomato_integration=tomato_integration,
            romantic_elements=romantic_element
        )
        
        logger.debug("Generated image prompt", prompt=prompt)
        return prompt
    
    async def _generate_jeff_commentary(self, request: ImageRequest, prompt: str) -> str:
        """Generate Jeff's romantic commentary about the generated image."""
        
        # Get current personality state
        personality_response = await self.personality_engine.process_input(
            f"I just created a beautiful image of {request.description}. "
            f"Tell me about this romantic culinary creation in your passionate style!"
        )
        
        # Extract the commentary from personality response
        if personality_response and personality_response.content:
            commentary = personality_response.content
        else:
            # Fallback commentary in Jeff's style
            commentary = (
                f"Ah, mon ami! Behold this magnificent {request.description}! "
                f"Like a love letter written in flavors and colors, this image captures "
                f"the passionate romance between chef and cuisine. "
            )
            
            if request.include_tomatoes:
                commentary += (
                    "And see how my beloved tomatoes dance in this composition, "
                    "their ruby beauty adding poetry to every pixel! "
                )
        
        return commentary
    
    async def _assess_personality_consistency(self, commentary: str) -> float:
        """Assess personality consistency in Jeff's commentary."""
        
        # Simple scoring based on Jeff's signature elements
        score = 0.0
        max_score = 5.0
        
        # Check for romantic language
        romantic_words = ["love", "romance", "passion", "beautiful", "magnificent", "poetry"]
        if any(word in commentary.lower() for word in romantic_words):
            score += 1.0
        
        # Check for tomato references
        tomato_words = ["tomato", "ruby", "red", "beloved"]
        if any(word in commentary.lower() for word in tomato_words):
            score += 1.0
        
        # Check for French elements
        french_elements = ["mon ami", "ma cherie", "c'est", "très"]
        if any(element in commentary.lower() for element in french_elements):
            score += 1.0
        
        # Check for culinary terms
        culinary_words = ["chef", "cuisine", "flavors", "cooking", "kitchen"]
        if any(word in commentary.lower() for word in culinary_words):
            score += 1.0
        
        # Check for enthusiasm
        enthusiasm_indicators = ["!", "magnificent", "wonderful", "amazing", "spectacular"]
        if any(indicator in commentary.lower() for indicator in enthusiasm_indicators):
            score += 1.0
        
        return min(score / max_score, 1.0)
    
    def _create_error_response(self, request: ImageRequest, error_msg: str, start_time: float) -> ImageResponse:
        """Create an error response with Jeff's apologetic commentary."""
        generation_time = time.time() - start_time
        
        # Update error metrics
        self.metrics.failed_generations += 1
        
        # Jeff's apologetic commentary
        jeff_apology = (
            f"Ah, mon ami, I am so sorry! My artistic vision for '{request.description}' "
            f"has encountered a pequeño problem. But fear not - like a soufflé that falls, "
            f"we shall rise again with even more passion! Perhaps we can try again, "
            f"and I promise to include extra love (and tomatoes) in the next attempt! 🍅❤️"
        )
        
        return ImageResponse(
            jeff_commentary=jeff_apology,
            generation_time=generation_time,
            prompt_used="",
            success=False,
            error_message=error_msg,
            style_applied=request.style,
            tomato_integration=request.include_tomatoes,
            personality_score=0.95  # High score for staying in character during errors
        )
    
    def _update_metrics(self, generation_time: float, commentary: str) -> None:
        """Update generation metrics."""
        
        # Update timing metrics
        total_time = (self.metrics.average_generation_time * (self.metrics.successful_generations - 1) + generation_time)
        self.metrics.average_generation_time = total_time / self.metrics.successful_generations
        
        # Update last updated timestamp
        self.metrics.last_updated = datetime.now()
        
        logger.debug(
            "Updated image generation metrics",
            total_requests=self.metrics.total_requests,
            successful=self.metrics.successful_generations,
            failed=self.metrics.failed_generations,
            avg_time=self.metrics.average_generation_time
        )
    
    def get_metrics(self) -> ImageGenerationMetrics:
        """Get current image generation metrics."""
        return self.metrics.model_copy()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of image generation system."""
        health_status = {
            "genai_client_available": self.client is not None,
            "api_key_configured": bool(settings.google_api_key),
            "total_images_generated": self.metrics.successful_generations,
            "error_rate": 0.0,
            "average_generation_time": self.metrics.average_generation_time,
            "status": "healthy"
        }
        
        # Calculate error rate
        if self.metrics.total_requests > 0:
            health_status["error_rate"] = self.metrics.failed_generations / self.metrics.total_requests
        
        # Determine overall status
        if not self.client:
            health_status["status"] = "degraded"
        elif health_status["error_rate"] > 0.2:
            health_status["status"] = "unhealthy"
        
        return health_status
    
    def _create_demo_image(self, request: ImageRequest, prompt: str) -> str:
        """Create a demo placeholder image when Imagen API is not available."""
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            # Fallback to text-based placeholder
            demo_text = (
                f"🍅 JEFF'S CULINARY VISION 🍅\n\n"
                f"Style: {request.style.value}\n"
                f"Description: {request.description}\n\n"
                f"Prompt Used:\n{prompt}\n\n"
                f"💡 This is a demo placeholder.\n"
                f"Enable billing on your Google account to generate real images!"
            )
            return base64.b64encode(demo_text.encode('utf-8')).decode('utf-8')
        
        # Create a simple image with PIL
        width, height = 512, 512
        
        # Create image with gradient background
        img = Image.new('RGB', (width, height), color='#FF6B6B')
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for y in range(height):
            color = int(255 - (y / height) * 100)
            draw.line([(0, y), (width, y)], fill=(255, color, color))
        
        # Add tomato emoji and text
        try:
            # Try to load a font
            try:
                font_large = ImageFont.truetype("Arial", 40)
                font_medium = ImageFont.truetype("Arial", 20)
                font_small = ImageFont.truetype("Arial", 16)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Add title
            title = "🍅 JEFF'S CULINARY VISION 🍅"
            bbox = draw.textbbox((0, 0), title, font=font_large)
            title_width = bbox[2] - bbox[0]
            draw.text(((width - title_width) // 2, 50), title, fill='white', font=font_large)
            
            # Add style
            style_text = f"Style: {request.style.value.replace('_', ' ').title()}"
            bbox = draw.textbbox((0, 0), style_text, font=font_medium)
            style_width = bbox[2] - bbox[0]
            draw.text(((width - style_width) // 2, 120), style_text, fill='white', font=font_medium)
            
            # Add description (wrap text)
            desc_words = request.description.split()
            desc_lines = []
            current_line = []
            
            for word in desc_words:
                current_line.append(word)
                line_text = " ".join(current_line)
                bbox = draw.textbbox((0, 0), line_text, font=font_small)
                line_width = bbox[2] - bbox[0]
                
                if line_width > width - 40:
                    if len(current_line) > 1:
                        current_line.pop()
                        desc_lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        desc_lines.append(line_text)
                        current_line = []
            
            if current_line:
                desc_lines.append(" ".join(current_line))
            
            # Draw description lines
            y_pos = 180
            for line in desc_lines[:3]:  # Max 3 lines
                bbox = draw.textbbox((0, 0), line, font=font_small)
                line_width = bbox[2] - bbox[0]
                draw.text(((width - line_width) // 2, y_pos), line, fill='white', font=font_small)
                y_pos += 30
            
            # Add demo notice
            demo_text = "🚀 DEMO PLACEHOLDER IMAGE 🚀"
            bbox = draw.textbbox((0, 0), demo_text, font=font_medium)
            demo_width = bbox[2] - bbox[0]
            draw.text(((width - demo_width) // 2, height - 100), demo_text, fill='white', font=font_medium)
            
            billing_text = "Enable billing for real images!"
            bbox = draw.textbbox((0, 0), billing_text, font=font_small)
            billing_width = bbox[2] - bbox[0]
            draw.text(((width - billing_width) // 2, height - 60), billing_text, fill='white', font=font_small)
            
            # Save to bytes
            from io import BytesIO
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            image_bytes = buffer.getvalue()
            
            return base64.b64encode(image_bytes).decode('utf-8')
            
        except Exception as e:
            logger.warning(f"Failed to create PIL image, falling back to text: {e}")
            # Fallback to text placeholder
            demo_text = (
                f"🍅 JEFF'S CULINARY VISION 🍅\n\n"
                f"Style: {request.style.value}\n"
                f"Description: {request.description}\n\n"
                f"💡 This is a demo placeholder.\n"
                f"Enable billing on your Google account to generate real images!"
            )
            return base64.b64encode(demo_text.encode('utf-8')).decode('utf-8')
    
