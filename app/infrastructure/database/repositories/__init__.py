"""Repository services - 서비스 단에서 관리."""

from .news_repository import NewsRepository
from .user_repository import UserRepository
from .email_repository import EmailRepository

__all__ = [
    "NewsRepository",
    "UserRepository", 
    "EmailRepository",
]
