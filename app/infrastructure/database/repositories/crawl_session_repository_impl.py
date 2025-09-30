"""크롤링 세션 레포지토리 구현체 - MongoDB를 사용한 실제 데이터 접근."""

from __future__ import annotations

from typing import List, Optional
from beanie import PydanticObjectId

from app.modules.crawling.entities import CrawlSession
from app.modules.crawling.repositories import CrawlSessionRepository


class CrawlSessionRepositoryImpl(CrawlSessionRepository):
    """크롤링 세션 레포지토리 구현체 - MongoDB 기반."""

    async def save(self, session: CrawlSession) -> str:
        """세션을 MongoDB에 저장합니다."""
        # TODO: 실제 MongoDB 저장 로직 구현
        return str(PydanticObjectId())

    async def get_by_id(self, session_id: str) -> Optional[CrawlSession]:
        """ID로 세션을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return None

    async def list_by_status(self, status: str) -> List[CrawlSession]:
        """상태별 세션 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []

    async def update_status(self, session_id: str, status: str, error_message: str = None) -> bool:
        """세션 상태를 업데이트합니다."""
        # TODO: 실제 MongoDB 업데이트 로직 구현
        return True
