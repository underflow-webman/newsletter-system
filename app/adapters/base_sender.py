"""기본 발송자 인터페이스 - 모든 발송자가 구현해야 하는 공통 인터페이스."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.modules.newsletter.entities import Newsletter


class BaseSender(ABC):
    """기본 발송자 인터페이스 - 모든 발송자가 구현해야 하는 공통 인터페이스."""
    
    def __init__(self, name: str):
        """발송자를 초기화합니다.
        
        Args:
            name: 발송자 이름
        """
        self.name = name
    
    @abstractmethod
    async def send(self, data: Any, **kwargs) -> bool:
        """데이터를 발송합니다.
        
        Args:
            data: 발송할 데이터
            **kwargs: 발송 옵션
            
        Returns:
            발송 성공 여부
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """발송자 상태를 확인합니다.
        
        Returns:
            발송자가 정상 작동하면 True, 그렇지 않으면 False
        """
        pass


class EmailSender(BaseSender):
    """이메일 발송자 기본 클래스."""
    
    @abstractmethod
    async def send_newsletter(self, newsletter: Newsletter, recipients: List[str]) -> bool:
        """뉴스레터를 이메일로 발송합니다.
        
        Args:
            newsletter: 발송할 뉴스레터
            recipients: 수신자 이메일 목록
            
        Returns:
            발송 성공 여부
        """
        pass
    
    @abstractmethod
    async def send_notification(self, subject: str, content: str, recipients: List[str]) -> bool:
        """알림을 이메일로 발송합니다.
        
        Args:
            subject: 이메일 제목
            content: 이메일 내용
            recipients: 수신자 이메일 목록
            
        Returns:
            발송 성공 여부
        """
        pass


class NotificationSender(BaseSender):
    """알림 발송자 기본 클래스."""
    
    @abstractmethod
    async def send_slack_message(self, message: str, channel: str) -> bool:
        """Slack 메시지를 발송합니다.
        
        Args:
            message: 발송할 메시지
            channel: 대상 채널
            
        Returns:
            발송 성공 여부
        """
        pass
    
    @abstractmethod
    async def send_webhook(self, url: str, data: Dict[str, Any]) -> bool:
        """웹훅을 발송합니다.
        
        Args:
            url: 웹훅 URL
            data: 발송할 데이터
            
        Returns:
            발송 성공 여부
        """
        pass
