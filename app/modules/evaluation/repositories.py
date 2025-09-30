"""평가 레포지토리 인터페이스들 - 평가 데이터 접근을 위한 추상화 계층 (구현체는 infrastructure에 있음)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .entities import EvaluationResult, EvaluationSession


class EvaluationResultRepository(ABC):
    """평가 결과 레포지토리 인터페이스 - 평가 결과 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, result: EvaluationResult) -> str:
        """평가 결과를 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_id(self, result_id: str) -> Optional[EvaluationResult]:
        """ID로 평가 결과를 조회합니다."""
        pass
    
    @abstractmethod
    async def get_by_post_id(self, post_id: str) -> Optional[EvaluationResult]:
        """게시글 ID로 평가 결과를 조회합니다."""
        pass
    
    @abstractmethod
    async def list_relevant_posts(self, min_score: float = 0.5) -> List[EvaluationResult]:
        """관련성 점수가 높은 게시글 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_category(self, category: str) -> List[EvaluationResult]:
        """특정 카테고리의 평가 결과 목록을 조회합니다."""
        pass


class EvaluationSessionRepository(ABC):
    """평가 세션 레포지토리 인터페이스 - 세션 데이터 접근 추상화."""
    
    @abstractmethod
    async def save(self, session: EvaluationSession) -> str:
        """세션을 데이터베이스에 저장합니다."""
        pass
    
    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[EvaluationSession]:
        """ID로 세션을 조회합니다."""
        pass
    
    @abstractmethod
    async def list_by_status(self, status: str) -> List[EvaluationSession]:
        """상태별 세션 목록을 조회합니다."""
        pass
    
    @abstractmethod
    async def update_status(self, session_id: str, status: str, error_message: str = None) -> bool:
        """세션 상태를 업데이트합니다."""
        pass
