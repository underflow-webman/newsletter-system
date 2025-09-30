"""이메일 서비스 설정."""

from pydantic_settings import BaseSettings
from typing import Optional


class EmailConfig(BaseSettings):
    """이메일 서비스 설정."""
    
    # Basic Email Configuration
    FROM_EMAIL: str = "noreply@yourdomain.com"
    FROM_NAME: str = "Newsletter System"
    
    # SMTP Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # SendGrid Configuration
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: Optional[str] = None
    
    # Daou Office Configuration
    DAOU_OFFICE_API_URL: str = "https://api.daouoffice.com"
    DAOU_OFFICE_API_KEY: Optional[str] = None
    DAOU_OFFICE_SECRET: Optional[str] = None
    
    # Default Email Provider
    DEFAULT_EMAIL_PROVIDER: str = "smtp"  # smtp, sendgrid, daou
    
    # Email Settings
    EMAIL_TIMEOUT: int = 30
    MAX_RECIPIENTS_PER_BATCH: int = 100
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


email_config = EmailConfig()
