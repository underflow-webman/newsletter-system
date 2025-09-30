"""설정 관리 모듈 - 모든 설정을 중앙에서 관리."""

from .app_config import app_config
from .database_config import database_config
from .llm_config import llm_config
from .email_config import email_config
from .crawling_config import crawling_config


class ConfigManager:
    """설정 관리자 - 모든 설정을 중앙에서 관리."""
    
    def __init__(self):
        self.app = app_config
        self.database = database_config
        self.llm = llm_config
        self.email = email_config
        self.crawling = crawling_config
    
    def get_all_settings(self) -> dict:
        """모든 설정을 딕셔너리로 반환합니다."""
        return {
            "app": self.app.dict(),
            "database": self.database.dict(),
            "llm": self.llm.dict(),
            "email": self.email.dict(),
            "crawling": self.crawling.dict(),
        }
    
    def validate_config(self) -> bool:
        """설정 유효성을 검증합니다."""
        try:
            # 필수 설정 검증
            if not self.database.MONGODB_URL:
                raise ValueError("MONGODB_URL is required")
            
            if not self.app.SECRET_KEY or self.app.SECRET_KEY == "your-secret-key-change-in-production":
                raise ValueError("SECRET_KEY must be set to a secure value")
            
            return True
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False


# 전역 설정 관리자 인스턴스
config = ConfigManager()

# 하위 호환성을 위한 기존 설정 객체들
settings = app_config  # 기존 코드와의 호환성
