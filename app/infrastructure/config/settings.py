from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application Configuration
    APP_NAME: str = "Newsletter System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "newsletter_system"
    
    # Daou Office API Configuration
    DAOU_OFFICE_API_URL: str = "https://api.daouoffice.com"
    DAOU_OFFICE_API_KEY: str = ""
    DAOU_OFFICE_SECRET: str = ""
    
    # Email Configuration
    FROM_EMAIL: str = "noreply@yourdomain.com"
    FROM_NAME: str = "Newsletter System"
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
