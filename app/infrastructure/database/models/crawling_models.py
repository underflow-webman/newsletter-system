"""크롤링 MongoDB 모델들 - Beanie ODM을 사용한 문서 모델 정의."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field
from enum import Enum


class PostType(str, Enum):
    """게시글 타입 열거형."""
    COMMUNITY = "community"
    NEWS = "news"
    GOVERNMENT = "government"


class CrawlStatus(str, Enum):
    """크롤링 상태 열거형."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CrawledPostDocument(Document):
    """크롤링된 게시글 문서 모델."""
    
    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    url: str = Field(..., unique=True, description="원본 URL")
    source: str = Field(..., description="출처 사이트")
    post_type: PostType = Field(..., description="게시글 타입")
    author: str = Field(..., description="작성자")
    views: int = Field(default=0, ge=0, description="조회수")
    likes: int = Field(default=0, ge=0, description="좋아요 수")
    comments: int = Field(default=0, ge=0, description="댓글 수")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="추가 메타데이터")
    crawled_at: datetime = Field(default_factory=datetime.utcnow, description="크롤링 시간")
    
    class Settings:
        name = "crawled_posts"
        indexes = [
            "source",
            "post_type",
            "crawled_at",
            "url",
        ]


class CrawlSessionDocument(Document):
    """크롤링 세션 문서 모델."""
    
    source: str = Field(..., description="크롤링 대상 사이트")
    post_type: PostType = Field(..., description="크롤링하는 게시글 타입")
    status: CrawlStatus = Field(default=CrawlStatus.PENDING, description="현재 상태")
    total_posts: int = Field(default=0, ge=0, description="전체 게시글 수")
    successful_posts: int = Field(default=0, ge=0, description="성공적으로 크롤링된 게시글 수")
    failed_posts: int = Field(default=0, ge=0, description="크롤링 실패한 게시글 수")
    started_at: datetime = Field(default_factory=datetime.utcnow, description="시작 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")
    error_message: Optional[str] = Field(None, description="에러 메시지")
    
    class Settings:
        name = "crawl_sessions"
        indexes = [
            "source",
            "post_type",
            "status",
            "started_at",
        ]
