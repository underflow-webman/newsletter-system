"""Ruliweb crawler - 루리웹 크롤러."""

from __future__ import annotations

from typing import List
from app.modules.crawling.entities import CrawledPost
from app.adapters.base_crawler import CommunityCrawler


class RuliwebCrawler(CommunityCrawler):
    """루리웹 크롤러 - 매우 직관적."""
    
    def __init__(self):
        super().__init__(
            base_url="https://bbs.ruliweb.com",
            name="ruliweb"
        )
    
    async def crawl(self, **kwargs) -> List[CrawledPost]:
        """크롤링을 수행합니다."""
        limit = kwargs.get('limit', 10)
        category = kwargs.get('category')
        
        if category:
            return await self.crawl_category(category, limit)
        else:
            return await self.crawl_hot_posts(limit)
    
    async def health_check(self) -> bool:
        """크롤러 상태를 확인합니다."""
        # TODO: 실제 헬스체크 로직 구현
        return True
    
    async def crawl_hot_posts(self, limit: int = 10) -> List[CrawledPost]:
        """인기 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
    
    async def crawl_category(self, category: str, limit: int = 10) -> List[CrawledPost]:
        """카테고리별 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
