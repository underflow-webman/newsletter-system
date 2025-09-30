"""평가 엔티티들 - 평가 시스템의 핵심 도메인 객체들."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class EvaluationStatus(Enum):
    """평가 상태 열거형."""
    PENDING = "pending"         # 대기 중
    IN_PROGRESS = "in_progress" # 진행 중
    COMPLETED = "completed"     # 완료
    FAILED = "failed"          # 실패


@dataclass
class EvaluationResult:
    """평가 결과 - 개별 게시글에 대한 평가 정보."""
    id: str                    # 평가 결과 고유 ID
    post_id: str               # 평가된 게시글 ID
    is_relevant: bool          # 관련성 여부
    category: str              # 분류된 카테고리
    relevance_score: float     # 관련성 점수 (0.0 ~ 1.0)
    confidence: float          # 신뢰도 (0.0 ~ 1.0)
    details: Dict[str, Any]    # 평가 세부 정보
    evaluated_at: datetime     # 평가 시간


@dataclass
class EvaluationSession:
    """평가 세션 - 한 번의 평가 작업을 추적하는 객체."""
    id: str                    # 세션 고유 ID
    total_posts: int           # 전체 게시글 수
    evaluated_posts: int       # 평가 완료된 게시글 수
    relevant_posts: int        # 관련성 있는 게시글 수
    irrelevant_posts: int      # 관련성 없는 게시글 수
    status: EvaluationStatus   # 현재 상태
    started_at: datetime       # 시작 시간
    completed_at: Optional[datetime]  # 완료 시간
    error_message: Optional[str]      # 에러 메시지
