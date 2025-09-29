from __future__ import annotations

from typing import List, Optional, Dict, Any

from app.domain.ports import ICrawler, CrawlTarget, RawPost


class GovBroadcastCommissionCrawler(ICrawler):
    """방송통신위원회 보도자료 크롤러(스텁)."""

    async def list_posts(self, target: CrawlTarget, options: Optional[Dict[str, Any]] = None) -> List[RawPost]:
        # TODO: Selenium으로 구현
        return []


