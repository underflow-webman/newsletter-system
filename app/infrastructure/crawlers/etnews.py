from __future__ import annotations

from typing import List, Optional, Dict, Any

from app.domain.ports import ICrawler, CrawlTarget, RawPost


class EtNewsCrawler(ICrawler):
    """전자신문 IT/통신 카테고리용 크롤러(스텁). Selenium 구현 지점."""

    async def list_posts(self, target: CrawlTarget, options: Optional[Dict[str, Any]] = None) -> List[RawPost]:
        # TODO: Selenium으로 구현
        return []


