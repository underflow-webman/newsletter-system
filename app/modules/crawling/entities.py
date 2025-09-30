"""크롤링 엔티티들 - 크롤링 시스템의 핵심 도메인 객체들."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class PostType(Enum):
    """게시글 타입 열거형."""
    COMMUNITY = "community"    # 커뮤니티 게시글
    NEWS = "news"             # 뉴스 기사
    GOVERNMENT = "government"  # 정부 문서


class CrawlStatus(Enum):
    """크롤링 상태 열거형."""
    PENDING = "pending"         # 대기 중
    IN_PROGRESS = "in_progress" # 진행 중
    COMPLETED = "completed"     # 완료
    FAILED = "failed"          # 실패


@dataclass
class CrawledPost:
    """크롤링된 게시글 - 웹사이트에서 수집한 게시글 정보."""
    id: str                    # 게시글 고유 ID
    title: str                 # 제목
    content: str               # 내용
    url: str                   # 원본 URL
    source: str                # 출처 사이트 (예: 뽐뿌, 루리웹)
    post_type: PostType        # 게시글 타입
    author: str                # 작성자
    views: int                 # 조회수
    likes: int                 # 좋아요 수
    comments: int              # 댓글 수
    metadata: Dict[str, Any]   # 추가 메타데이터
    crawled_at: datetime       # 크롤링 시간


@dataclass
class CrawlSession:
    """크롤링 세션 - 한 번의 크롤링 작업을 추적하는 객체."""
    id: str                    # 세션 고유 ID
    source: str                # 크롤링 대상 사이트
    post_type: PostType        # 크롤링하는 게시글 타입
    status: CrawlStatus        # 현재 상태
    total_posts: int           # 전체 게시글 수
    successful_posts: int      # 성공적으로 크롤링된 게시글 수
    failed_posts: int          # 크롤링 실패한 게시글 수
    started_at: datetime       # 시작 시간
    completed_at: Optional[datetime]  # 완료 시간
    error_message: Optional[str]      # 에러 메시지
