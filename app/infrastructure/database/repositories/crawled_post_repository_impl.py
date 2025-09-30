"""크롤링된 게시글 레포지토리 구현체 - MongoDB를 사용한 실제 데이터 접근."""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.modules.crawling.entities import CrawledPost, PostType
from app.modules.crawling.repositories import CrawledPostRepository


class CrawledPostRepositoryImpl(CrawledPostRepository):
    """크롤링된 게시글 레포지토리 구현체 - MongoDB 기반."""

    async def save(self, post: CrawledPost) -> str:
        """게시글을 MongoDB에 저장합니다."""
        # TODO: 실제 MongoDB 저장 로직 구현
        return str(PydanticObjectId())

    async def get_by_id(self, post_id: str) -> Optional[CrawledPost]:
        """ID로 게시글을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return None

    async def list_by_source(self, source: str) -> List[CrawledPost]:
        """특정 소스의 게시글 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []

    async def list_by_type(self, post_type: PostType) -> List[CrawledPost]:
        """특정 타입의 게시글 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []

    async def list_recent(self, limit: int = 100) -> List[CrawledPost]:
        """최근 크롤링된 게시글 목록을 조회합니다."""
        # TODO: 실제 MongoDB 조회 로직 구현
        return []
