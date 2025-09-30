"""뉴스레터 엔티티들 - 뉴스레터 시스템의 핵심 도메인 객체들."""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class NewsletterStatus(Enum):
    """뉴스레터 상태 열거형."""
    DRAFT = "draft"          # 초안
    SCHEDULED = "scheduled"  # 예약됨
    SENT = "sent"           # 발송됨
    FAILED = "failed"       # 실패


@dataclass
class NewsletterItem:
    """뉴스레터 아이템 - 뉴스레터에 포함되는 개별 뉴스 아이템."""
    id: str                  # 아이템 고유 ID
    title: str               # 제목
    content: str             # 내용
    source: str              # 출처 (예: 뽐뿌, 루리웹)
    url: str                 # 원본 URL
    category: str            # 카테고리 (예: SKT, KT, LGU)
    relevance_score: float   # 관련성 점수 (0.0 ~ 1.0)
    created_at: datetime     # 생성 시간


@dataclass
class Newsletter:
    """뉴스레터 - 뉴스레터 전체를 나타내는 엔티티."""
    id: str                          # 뉴스레터 고유 ID
    title: str                       # 뉴스레터 제목
    items: List[NewsletterItem]      # 포함된 뉴스 아이템들
    status: NewsletterStatus         # 현재 상태
    scheduled_at: Optional[datetime] # 예약 발송 시간
    sent_at: Optional[datetime]      # 실제 발송 시간
    created_at: datetime             # 생성 시간
    updated_at: datetime             # 마지막 수정 시간


@dataclass
class Subscriber:
    """구독자 - 뉴스레터를 구독하는 사용자."""
    id: str                          # 구독자 고유 ID
    email: str                       # 이메일 주소
    name: str                        # 이름
    categories: List[str]            # 관심 카테고리 목록
    is_active: bool                  # 활성 구독 여부
    subscribed_at: datetime          # 구독 시작 시간
    unsubscribed_at: Optional[datetime]  # 구독 해지 시간
