"""Clien crawler - 클리앙 크롤러."""

from __future__ import annotations

from typing import List
from app.modules.crawling.entities import CrawledPost


class ClienCrawler:
    """클리앙 크롤러 - 매우 직관적."""
    
    def __init__(self):
        self.base_url = "https://www.clien.net"
        self.name = "clien"
    
    async def crawl_hot_posts(self) -> List[CrawledPost]:
        """인기 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
    
    async def crawl_category(self, category: str) -> List[CrawledPost]:
        """카테고리별 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
