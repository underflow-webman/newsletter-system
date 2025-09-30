"""뉴스레터 MongoDB 모델들 - Beanie ODM을 사용한 문서 모델 정의."""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field
from enum import Enum


class NewsletterStatus(str, Enum):
    """뉴스레터 상태 열거형."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    FAILED = "failed"


class NewsletterItemDocument(Document):
    """뉴스레터 아이템 문서 모델."""
    
    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    source: str = Field(..., description="출처")
    url: str = Field(..., description="원본 URL")
    category: str = Field(..., description="카테고리")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="관련성 점수")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="생성 시간")
    
    class Settings:
        name = "newsletter_items"


class NewsletterDocument(Document):
    """뉴스레터 문서 모델."""
    
    title: str = Field(..., description="뉴스레터 제목")
    items: List[NewsletterItemDocument] = Field(default_factory=list, description="포함된 뉴스 아이템들")
    status: NewsletterStatus = Field(default=NewsletterStatus.DRAFT, description="현재 상태")
    scheduled_at: Optional[datetime] = Field(None, description="예약 발송 시간")
    sent_at: Optional[datetime] = Field(None, description="실제 발송 시간")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="생성 시간")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="마지막 수정 시간")
    
    class Settings:
        name = "newsletters"
        indexes = [
            "status",
            "created_at",
            "scheduled_at",
        ]


class SubscriberDocument(Document):
    """구독자 문서 모델."""
    
    email: str = Field(..., unique=True, description="이메일 주소")
    name: str = Field(..., description="이름")
    categories: List[str] = Field(default_factory=list, description="관심 카테고리 목록")
    is_active: bool = Field(default=True, description="활성 구독 여부")
    subscribed_at: datetime = Field(default_factory=datetime.utcnow, description="구독 시작 시간")
    unsubscribed_at: Optional[datetime] = Field(None, description="구독 해지 시간")
    
    class Settings:
        name = "subscribers"
        indexes = [
            "email",
            "is_active",
            "subscribed_at",
        ]
