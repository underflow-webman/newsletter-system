"""데이터베이스 설정."""

from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    """데이터베이스 설정."""
    
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "newsletter_system"
    
    # Connection Pool Settings
    MAX_POOL_SIZE: int = 10
    MIN_POOL_SIZE: int = 1
    MAX_IDLE_TIME_MS: int = 30000
    
    # Query Settings
    QUERY_TIMEOUT_MS: int = 30000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


database_config = DatabaseConfig()
