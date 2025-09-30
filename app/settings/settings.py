"""애플리케이션 통합 설정 - 모든 설정을 하나로 관리합니다."""

from pydantic_settings import BaseSettings
from typing import List
from app.infrastructure.config.app_config import app_config
from app.infrastructure.config.database_config import database_config
from app.infrastructure.config.email_config import email_config
from app.infrastructure.config.llm_config import llm_config
from app.infrastructure.config.crawling_config import crawling_config


class Settings(BaseSettings):
    """애플리케이션 통합 설정 클래스 - 모든 설정을 하나로 관리합니다."""
    
    # 애플리케이션 설정
    APP_NAME: str = app_config.APP_NAME
    APP_VERSION: str = app_config.APP_VERSION
    DEBUG: bool = app_config.DEBUG
    SECRET_KEY: str = app_config.SECRET_KEY
    
    # 서버 설정
    HOST: str = app_config.HOST
    PORT: int = app_config.PORT
    
    # CORS 설정
    ALLOWED_ORIGINS: List[str] = app_config.ALLOWED_ORIGINS
    
    # 데이터베이스 설정
    MONGODB_URL: str = database_config.MONGODB_URL
    DATABASE_NAME: str = database_config.DATABASE_NAME
    MAX_POOL_SIZE: int = database_config.MAX_POOL_SIZE
    MIN_POOL_SIZE: int = database_config.MIN_POOL_SIZE
    MAX_IDLE_TIME_MS: int = database_config.MAX_IDLE_TIME_MS
    QUERY_TIMEOUT_MS: int = database_config.QUERY_TIMEOUT_MS
    
    # 이메일 설정
    EMAIL_PROVIDER: str = email_config.DEFAULT_EMAIL_PROVIDER
    EMAIL_FROM_ADDRESS: str = email_config.FROM_EMAIL
    EMAIL_FROM_NAME: str = email_config.FROM_NAME
    
    # LLM 설정
    LLM_PROVIDER: str = llm_config.DEFAULT_LLM_PROVIDER
    LLM_MODEL: str = llm_config.OPENAI_MODEL
    LLM_API_KEY: str = llm_config.OPENAI_API_KEY or ""
    
    # 크롤링 설정
    CRAWL_INTERVAL_MINUTES: int = 60
    CRAWL_BATCH_SIZE: int = crawling_config.DEFAULT_CRAWL_LIMIT
    CRAWL_TIMEOUT_SECONDS: int = crawling_config.CRAWL_TIMEOUT
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()
