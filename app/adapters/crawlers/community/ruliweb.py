"""Ruliweb crawler - 루리웹 크롤러."""

from __future__ import annotations

from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CrawledPost:
    """크롤링된 게시글."""
    title: str
    content: str
    url: str
    author: str
    views: int
    likes: int
    comments: int
    crawled_at: datetime


class RuliwebCrawler:
    """루리웹 크롤러 - 매우 직관적."""
    
    def __init__(self):
        self.base_url = "https://bbs.ruliweb.com"
        self.name = "ruliweb"
    
    async def crawl_hot_posts(self) -> List[CrawledPost]:
        """인기 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
    
    async def crawl_category(self, category: str) -> List[CrawledPost]:
        """카테고리별 게시글 크롤링."""
        # TODO: 실제 크롤링 로직
        return []
