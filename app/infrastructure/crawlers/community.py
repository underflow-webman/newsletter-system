from __future__ import annotations

from typing import List, Optional, Dict, Any

from app.domain.ports import ICrawler, CrawlTarget, RawPost


class CommunityCrawler(ICrawler):
    """커뮤니티 여론 크롤러(스텁). 사이트별로 추가 구현."""

    async def list_posts(self, target: CrawlTarget, options: Optional[Dict[str, Any]] = None) -> List[RawPost]:
        # TODO: Selenium으로 구현
        return []


