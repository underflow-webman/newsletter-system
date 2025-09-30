"""크롤링 레포지토리 인터페이스들 - 크롤링 데이터 접근을 위한 추상화 계층 (구현체는 infrastructure에 있음)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .entities import CrawledPost, CrawlSession, PostType


class CrawledPostRepository(ABC):
    """크롤링된 게시글 레포지토리 인터페이스 - 게시글 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, post: CrawledPost) -> str:
        """게시글을 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_id(self, post_id: str) -> Optional[CrawledPost]:
        """ID로 게시글을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_source(self, source: str) -> List[CrawledPost]:
        """특정 소스의 게시글 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_type(self, post_type: PostType) -> List[CrawledPost]:
        """특정 타입의 게시글 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_recent(self, limit: int = 100) -> List[CrawledPost]:
        """최근 크롤링된 게시글 목록을 조회합니다."""
        pass


class CrawlSessionRepository(ABC):
    """크롤링 세션 레포지토리 인터페이스 - 세션 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, session: CrawlSession) -> str:
        """세션을 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[CrawlSession]:
        """ID로 세션을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_status(self, status: str) -> List[CrawlSession]:
        """상태별 세션 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def update_status(self, session_id: str, status: str, error_message: str = None) -> bool:
        """세션 상태를 업데이트합니다."""
        pass
