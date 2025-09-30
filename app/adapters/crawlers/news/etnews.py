"""ETNews crawler - 전자신문 크롤러."""

from __future__ import annotations

from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class NewsArticle:
    """뉴스 기사."""
    title: str
    content: str
    url: str
    author: str
    published_at: datetime
    category: str


class EtnewsCrawler:
    """전자신문 크롤러."""
    
    def __init__(self):
        self.base_url = "https://www.etnews.com"
        self.name = "etnews"
    
    async def crawl_tech_news(self) -> List[NewsArticle]:
        """IT 뉴스를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
    
    async def crawl_telecom_news(self) -> List[NewsArticle]:
        """통신 뉴스를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
