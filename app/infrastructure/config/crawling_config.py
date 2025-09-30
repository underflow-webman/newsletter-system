"""크롤링 설정."""

from pydantic_settings import BaseSettings
from typing import Dict, Any


class CrawlingConfig(BaseSettings):
    """크롤링 설정."""
    
    # General Crawling Settings
    DEFAULT_CRAWL_LIMIT: int = 10
    MAX_CONCURRENT_CRAWLS: int = 5
    CRAWL_TIMEOUT: int = 30
    REQUEST_DELAY: float = 1.0  # seconds between requests
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Retry Settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 2.0
    
    # User Agent
    USER_AGENT: str = "Newsletter System Bot 1.0"
    
    # Community Crawling Settings
    COMMUNITY_HOT_POSTS_LIMIT: int = 20
    COMMUNITY_CATEGORY_LIMIT: int = 10
    
    # News Crawling Settings
    NEWS_TECH_LIMIT: int = 15
    NEWS_TELECOM_LIMIT: int = 15
    
    # Government Crawling Settings
    GOV_NOTICES_LIMIT: int = 10
    GOV_POLICIES_LIMIT: int = 10
    
    # Site-specific Settings
    SITE_SETTINGS: Dict[str, Any] = {
        "ppomppu": {
            "base_url": "https://www.ppomppu.co.kr",
            "rate_limit": 30,  # requests per minute
            "timeout": 15
        },
        "ruliweb": {
            "base_url": "https://bbs.ruliweb.com",
            "rate_limit": 30,
            "timeout": 15
        },
        "etnews": {
            "base_url": "https://www.etnews.com",
            "rate_limit": 20,
            "timeout": 20
        }
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


crawling_config = CrawlingConfig()
