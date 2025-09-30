"""Crawling services - 크롤링 서비스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import CrawledPost, CrawlSession, PostType, CrawlStatus
from .repositories import CrawledPostRepository, CrawlSessionRepository


class CrawlingService:
    """크롤링 서비스."""
    
    def __init__(self, post_repo: CrawledPostRepository, session_repo: CrawlSessionRepository):
        self.post_repo = post_repo
        self.session_repo = session_repo
    
    async def start_crawl_session(self, source: str, post_type: PostType) -> CrawlSession:
        """크롤링 세션을 시작합니다."""
        session = CrawlSession(
            id=f"session_{datetime.utcnow().timestamp()}",
            source=source,
            post_type=post_type,
            status=CrawlStatus.PENDING,
            total_posts=0,
            successful_posts=0,
            failed_posts=0,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None
        )
        
        await self.session_repo.save(session)
        return session
    
    async def save_crawled_post(self, post: CrawledPost) -> str:
        """크롤링된 게시글을 저장합니다."""
        return await self.post_repo.save(post)
    
    async def complete_crawl_session(self, session_id: str, total_posts: int, successful_posts: int, failed_posts: int) -> bool:
        """크롤링 세션을 완료합니다."""
        return await self.session_repo.update_status(
            session_id, 
            CrawlStatus.COMPLETED.value,
            f"Total: {total_posts}, Success: {successful_posts}, Failed: {failed_posts}"
        )
    
    async def fail_crawl_session(self, session_id: str, error_message: str) -> bool:
        """크롤링 세션을 실패로 처리합니다."""
        return await self.session_repo.update_status(
            session_id,
            CrawlStatus.FAILED.value,
            error_message
        )


class DataExtractionService:
    """데이터 추출 서비스."""
    
    async def extract_post_data(self, raw_data: Dict[str, Any], source: str, post_type: PostType) -> CrawledPost:
        """원시 데이터에서 게시글 데이터를 추출합니다."""
        return CrawledPost(
            id=f"post_{datetime.utcnow().timestamp()}",
            title=raw_data.get("title", ""),
            content=raw_data.get("content", ""),
            url=raw_data.get("url", ""),
            source=source,
            post_type=post_type,
            author=raw_data.get("author", ""),
            views=raw_data.get("views", 0),
            likes=raw_data.get("likes", 0),
            comments=raw_data.get("comments", 0),
            metadata=raw_data.get("metadata", {}),
            crawled_at=datetime.utcnow()
        )
