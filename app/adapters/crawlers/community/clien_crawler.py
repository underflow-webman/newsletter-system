"""클리앙 크롤러 - 클리앙 커뮤니티에서 게시글을 크롤링하는 클래스."""

from __future__ import annotations

from typing import List
from app.modules.crawling.entities import CrawledPost


class ClienCrawler:
    """클리앙 크롤러 - 클리앙 커뮤니티에서 게시글을 수집합니다."""
    
    def __init__(self):
        """클리앙 크롤러를 초기화합니다."""
        self.base_url = "https://www.clien.net"
        self.name = "clien"
    
    async def crawl_hot_posts(self) -> List[CrawledPost]:
        """인기 게시글을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
    
    async def crawl_category(self, category: str) -> List[CrawledPost]:
        """특정 카테고리의 게시글을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
