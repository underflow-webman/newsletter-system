from __future__ import annotations

from typing import List, Optional, Dict, Any

from app.domain.ports import ICrawler, CrawlTarget, RawPost


class SimpleListCrawler(ICrawler):
    """기본 샘플 크롤러(데모용)."""

    async def list_posts(self, target: CrawlTarget, options: Optional[Dict[str, Any]] = None) -> List[RawPost]:
        return [
            RawPost(
                source_name=target.source_name,
                url=f"https://example.com/{i}",
                title=f"{target.source_name} 통신시장 뉴스 {i}",
                content_snippet="5G 투자와 요금제 개편 관련 소식.",
            )
            for i in range(min(target.limit, 5))
        ]


