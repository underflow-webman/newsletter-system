"""LLM 서비스 설정."""

from pydantic_settings import BaseSettings
from typing import Optional


class LLMConfig(BaseSettings):
    """LLM 서비스 설정."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Claude Configuration
    CLAUDE_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    CLAUDE_MAX_TOKENS: int = 2000
    
    # Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_MAX_TOKENS: int = 2000
    
    # Default LLM Provider
    DEFAULT_LLM_PROVIDER: str = "openai"  # openai, claude, gemini
    
    # Request Settings
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


llm_config = LLMConfig()
