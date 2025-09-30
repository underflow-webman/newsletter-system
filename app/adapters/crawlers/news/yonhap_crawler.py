"""Yonhap crawler - 연합뉴스 크롤러."""

from __future__ import annotations

from typing import List
from app.modules.crawling.entities import NewsArticle


class YonhapCrawler:
    """연합뉴스 크롤러."""
    
    def __init__(self):
        self.base_url = "https://www.yna.co.kr"
        self.name = "yonhap"
    
    async def crawl_tech_news(self) -> List[NewsArticle]:
        """IT 뉴스를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
    
    async def crawl_telecom_news(self) -> List[NewsArticle]:
        """통신 뉴스를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
