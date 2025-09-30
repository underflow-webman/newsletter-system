"""평가 레포지토리 구현체 - MongoDB를 사용한 실제 데이터 접근."""

from __future__ import annotations

from typing import List, Optional
from beanie import PydanticObjectId

from app.modules.evaluation.entities import EvaluationResult, EvaluationSession
from app.modules.evaluation.repositories import EvaluationResultRepository, EvaluationSessionRepository


class EvaluationResultRepositoryImpl(EvaluationResultRepository):
    """평가 결과 레포지토리 구현체 - MongoDB 기반."""

    async def save(self, result: EvaluationResult) -> str:
        """평가 결과를 MongoDB에 저장합니다."""
        # TODO: 실제 MongoDB 저장 로직 구현
        return str(PydanticObjectId())

    async def get_by_id(self, result_id: str) -> Optional[EvaluationResult]:
        """ID로 평가 결과를 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return None

    async def get_by_post_id(self, post_id: str) -> Optional[EvaluationResult]:
        """게시글 ID로 평가 결과를 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return None

    async def list_relevant_posts(self, min_score: float = 0.5) -> List[EvaluationResult]:
        """관련성 점수가 높은 게시글 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []

    async def list_by_category(self, category: str) -> List[EvaluationResult]:
        """특정 카테고리의 평가 결과 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []


class EvaluationSessionRepositoryImpl(EvaluationSessionRepository):
    """평가 세션 레포지토리 구현체 - MongoDB 기반."""

    async def save(self, session: EvaluationSession) -> str:
        """세션을 MongoDB에 저장합니다."""
        # TODO: 실제 MongoDB 저장 로직 구현
        return str(PydanticObjectId())

    async def get_by_id(self, session_id: str) -> Optional[EvaluationSession]:
        """ID로 세션을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return None

    async def list_by_status(self, status: str) -> List[EvaluationSession]:
        """상태별 세션 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []

    async def update_status(self, session_id: str, status: str, error_message: str = None) -> bool:
        """세션 상태를 업데이트합니다."""
        # TODO: 실제 MongoDB 업데이트 로직 구현
        return True
