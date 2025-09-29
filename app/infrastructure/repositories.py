from __future__ import annotations

from typing import List, Dict

from app.domain.ports import INewsRepository, RawPost


class InMemoryNewsRepository(INewsRepository):
    """초기 통합 테스트를 위한 인메모리 저장소 구현."""

    def __init__(self) -> None:
        self._raw_posts: List[RawPost] = []
        self._drafts: List[Dict] = []

    async def save_raw_posts(self, posts: List[RawPost]) -> int:
        """원시 포스트를 단순 누적 저장."""
        before = len(self._raw_posts)
        self._raw_posts.extend(posts)
        return len(self._raw_posts) - before

    async def save_newsletter_draft(self, draft: Dict) -> str:
        """뉴스레터 초안 저장 후 식별자(인덱스 기반 문자열) 반환."""
        self._drafts.append(draft)
        return str(len(self._drafts))


