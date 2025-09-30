"""Crawling use cases - 크롤링 유즈케이스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import CrawledPost, PostType
from .services import CrawlingService, DataExtractionService
from .repositories import CrawledPostRepository, CrawlSessionRepository


class CrawlCommunityUseCase:
    """커뮤니티 크롤링 유즈케이스."""
    
    def __init__(self, crawling_service: CrawlingService, extraction_service: DataExtractionService):
        self.crawling_service = crawling_service
        self.extraction_service = extraction_service
    
    async def execute(self, source: str, raw_data: List[Dict[str, Any]]) -> List[CrawledPost]:
        """커뮤니티를 크롤링합니다."""
        # 크롤링 세션 시작
        session = await self.crawling_service.start_crawl_session(source, PostType.COMMUNITY)
        
        crawled_posts = []
        successful_posts = 0
        failed_posts = 0
        
        try:
            for data in raw_data:
                try:
                    # 데이터 추출
                    post = await self.extraction_service.extract_post_data(data, source, PostType.COMMUNITY)
                    
                    # 저장
                    await self.crawling_service.save_crawled_post(post)
                    crawled_posts.append(post)
                    successful_posts += 1
                    
                except Exception as e:
                    print(f"Failed to process post: {e}")
                    failed_posts += 1
            
            # 세션 완료
            await self.crawling_service.complete_crawl_session(
                session.id, 
                len(raw_data), 
                successful_posts, 
                failed_posts
            )
            
        except Exception as e:
            # 세션 실패
            await self.crawling_service.fail_crawl_session(session.id, str(e))
            raise
        
        return crawled_posts


class CrawlNewsUseCase:
    """뉴스 크롤링 유즈케이스."""
    
    def __init__(self, crawling_service: CrawlingService, extraction_service: DataExtractionService):
        self.crawling_service = crawling_service
        self.extraction_service = extraction_service
    
    async def execute(self, source: str, raw_data: List[Dict[str, Any]]) -> List[CrawledPost]:
        """뉴스를 크롤링합니다."""
        # 크롤링 세션 시작
        session = await self.crawling_service.start_crawl_session(source, PostType.NEWS)
        
        crawled_posts = []
        successful_posts = 0
        failed_posts = 0
        
        try:
            for data in raw_data:
                try:
                    # 데이터 추출
                    post = await self.extraction_service.extract_post_data(data, source, PostType.NEWS)
                    
                    # 저장
                    await self.crawling_service.save_crawled_post(post)
                    crawled_posts.append(post)
                    successful_posts += 1
                    
                except Exception as e:
                    print(f"Failed to process post: {e}")
                    failed_posts += 1
            
            # 세션 완료
            await self.crawling_service.complete_crawl_session(
                session.id, 
                len(raw_data), 
                successful_posts, 
                failed_posts
            )
            
        except Exception as e:
            # 세션 실패
            await self.crawling_service.fail_crawl_session(session.id, str(e))
            raise
        
        return crawled_posts


class CrawlGovernmentUseCase:
    """정부 크롤링 유즈케이스."""
    
    def __init__(self, crawling_service: CrawlingService, extraction_service: DataExtractionService):
        self.crawling_service = crawling_service
        self.extraction_service = extraction_service
    
    async def execute(self, source: str, raw_data: List[Dict[str, Any]]) -> List[CrawledPost]:
        """정부 기관을 크롤링합니다."""
        # 크롤링 세션 시작
        session = await self.crawling_service.start_crawl_session(source, PostType.GOVERNMENT)
        
        crawled_posts = []
        successful_posts = 0
        failed_posts = 0
        
        try:
            for data in raw_data:
                try:
                    # 데이터 추출
                    post = await self.extraction_service.extract_post_data(data, source, PostType.GOVERNMENT)
                    
                    # 저장
                    await self.crawling_service.save_crawled_post(post)
                    crawled_posts.append(post)
                    successful_posts += 1
                    
                except Exception as e:
                    print(f"Failed to process post: {e}")
                    failed_posts += 1
            
            # 세션 완료
            await self.crawling_service.complete_crawl_session(
                session.id, 
                len(raw_data), 
                successful_posts, 
                failed_posts
            )
            
        except Exception as e:
            # 세션 실패
            await self.crawling_service.fail_crawl_session(session.id, str(e))
            raise
        
        return crawled_posts
