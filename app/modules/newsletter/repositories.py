"""뉴스레터 레포지토리 인터페이스들 - 뉴스레터 데이터 접근을 위한 추상화 계층 (구현체는 infrastructure에 있음)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .entities import Newsletter, NewsletterItem, Subscriber


class NewsletterRepository(ABC):
    """뉴스레터 레포지토리 인터페이스 - 뉴스레터 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, newsletter: Newsletter) -> str:
        """뉴스레터를 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_id(self, newsletter_id: str) -> Optional[Newsletter]:
        """ID로 뉴스레터를 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_status(self, status: str) -> List[Newsletter]:
        """상태별 뉴스레터 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def update_status(self, newsletter_id: str, status: str) -> bool:
        """뉴스레터 상태를 업데이트합니다."""
        pass


class SubscriberRepository(ABC):
    """구독자 레포지토리 인터페이스 - 구독자 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, subscriber: Subscriber) -> str:
        """구독자를 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Subscriber]:
        """이메일로 구독자를 조회합니다."""
        pass
    
    @abstractmethod
    async def list_active(self) -> List[Subscriber]:
        """활성 구독자 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def unsubscribe(self, email: str) -> bool:
        """구독을 해지합니다."""
        pass
