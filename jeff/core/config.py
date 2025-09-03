"""Configuration management for Jeff the Chef."""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    
    # Database Configuration
    database_url: str = Field("sqlite:///./jeff_chef.db", env="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # Application Configuration
    env: str = Field("development", env="ENV")
    debug: bool = Field(True, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    
    # Jeff's Personality Configuration
    jeff_tomato_obsession_level: int = Field(9, env="JEFF_TOMATO_OBSESSION_LEVEL", ge=1, le=10)
    jeff_romantic_intensity: int = Field(8, env="JEFF_ROMANTIC_INTENSITY", ge=1, le=10)
    jeff_base_energy_level: int = Field(7, env="JEFF_BASE_ENERGY_LEVEL", ge=1, le=10)
    jeff_creativity_multiplier: float = Field(1.5, env="JEFF_CREATIVITY_MULTIPLIER", ge=0.1, le=3.0)
    
    # Quality Thresholds
    personality_consistency_threshold: float = Field(0.90, env="PERSONALITY_CONSISTENCY_THRESHOLD")
    content_quality_threshold: float = Field(0.85, env="CONTENT_QUALITY_THRESHOLD")
    response_time_threshold: float = Field(2.0, env="RESPONSE_TIME_THRESHOLD")
    
    # Security
    secret_key: str = Field("development-secret-key", env="SECRET_KEY")
    cors_origins: List[str] = Field(
        ["http://localhost:3000", "http://localhost:8000"], 
        env="CORS_ORIGINS"
    )
    
    # Feature Flags
    enable_memory_system: bool = Field(True, env="ENABLE_MEMORY_SYSTEM")
    enable_image_generation: bool = Field(True, env="ENABLE_IMAGE_GENERATION")
    enable_multi_platform: bool = Field(True, env="ENABLE_MULTI_PLATFORM")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()