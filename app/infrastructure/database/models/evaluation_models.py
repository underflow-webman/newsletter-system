"""평가 MongoDB 모델들 - Beanie ODM을 사용한 문서 모델 정의."""

from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field
from enum import Enum


class EvaluationStatus(str, Enum):
    """평가 상태 열거형."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EvaluationResultDocument(Document):
    """평가 결과 문서 모델."""
    
    post_id: str = Field(..., description="평가된 게시글 ID")
    is_relevant: bool = Field(..., description="관련성 여부")
    category: str = Field(..., description="분류된 카테고리")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="관련성 점수")
    confidence: float = Field(..., ge=0.0, le=1.0, description="신뢰도")
    details: Dict[str, Any] = Field(default_factory=dict, description="평가 세부 정보")
    evaluated_at: datetime = Field(default_factory=datetime.utcnow, description="평가 시간")
    
    class Settings:
        name = "evaluation_results"
        indexes = [
            "post_id",
            "is_relevant",
            "category",
            "relevance_score",
            "evaluated_at",
        ]


class EvaluationSessionDocument(Document):
    """평가 세션 문서 모델."""
    
    total_posts: int = Field(default=0, ge=0, description="전체 게시글 수")
    evaluated_posts: int = Field(default=0, ge=0, description="평가 완료된 게시글 수")
    relevant_posts: int = Field(default=0, ge=0, description="관련성 있는 게시글 수")
    irrelevant_posts: int = Field(default=0, ge=0, description="관련성 없는 게시글 수")
    status: EvaluationStatus = Field(default=EvaluationStatus.PENDING, description="현재 상태")
    started_at: datetime = Field(default_factory=datetime.utcnow, description="시작 시간")
    completed_at: Optional[datetime] = Field(None, description="완료 시간")
    error_message: Optional[str] = Field(None, description="에러 메시지")
    
    class Settings:
        name = "evaluation_sessions"
        indexes = [
            "status",
            "started_at",
        ]
