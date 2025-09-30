"""뽐뿌 크롤러 - 뽐뿌 커뮤니티에서 게시글을 크롤링하는 클래스."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CrawledPost:
    """크롤링된 게시글 - 웹사이트에서 수집한 게시글 정보."""
    title: str                 # 게시글 제목
    content: str               # 게시글 내용
    url: str                   # 원본 URL
    author: str                # 작성자
    views: int                 # 조회수
    likes: int                 # 좋아요 수
    comments: int              # 댓글 수
    crawled_at: datetime       # 크롤링 시간


class PpomppuCrawler:
    """뽐뿌 크롤러 - 뽐뿌 커뮤니티에서 게시글을 수집합니다."""
    
    def __init__(self):
        self.base_url = "https://www.ppomppu.co.kr"  # 뽐뿌 기본 URL
        self.name = "ppomppu"                         # 크롤러 이름
    
    async def crawl_hot_posts(self) -> List[CrawledPost]:
        """인기 게시글을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현 (Selenium, requests 등 사용)
        return [
            CrawledPost(
                title="뽐뿌 핫 게시글 1",
                content="뽐뿌 게시글 내용",
                url=f"{self.base_url}/hot/1",
                author="user1",
                views=100,
                likes=5,
                comments=2,
                crawled_at=datetime.utcnow()
            )
        ]
    
    async def crawl_category(self, category: str) -> List[CrawledPost]:
        """특정 카테고리의 게시글을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
