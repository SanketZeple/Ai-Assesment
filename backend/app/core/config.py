"""
Configuration settings for the application
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Document Summarizer"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI dev server
    ]
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/summarizer_db"
    )
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["text/plain", "text/csv", "application/pdf"]
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # LLM Settings
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1000"))
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    
    # Retry Settings
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "2"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "1"))  # seconds
    
    # Application - store as string and convert to bool
    DEBUG: str = "false"
    
    @property
    def debug_mode(self) -> bool:
        """Convert DEBUG string to boolean"""
        debug_str = self.DEBUG.lower()
        if debug_str in ("true", "1", "yes", "on"):
            return True
        elif debug_str in ("false", "0", "no", "off", "release"):
            return False
        else:
            return False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()