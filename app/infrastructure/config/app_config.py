"""애플리케이션 기본 설정."""

from pydantic_settings import BaseSettings
from typing import List


class AppConfig(BaseSettings):
    """애플리케이션 기본 설정."""
    
    # Application Configuration
    APP_NAME: str = "Newsletter System"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


app_config = AppConfig()
