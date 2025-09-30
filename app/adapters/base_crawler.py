"""기본 크롤러 인터페이스 - 모든 크롤러가 구현해야 하는 공통 인터페이스."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.modules.crawling.entities import CrawledPost, NewsArticle, GovernmentDocument


class BaseCrawler(ABC):
    """기본 크롤러 인터페이스 - 모든 크롤러가 구현해야 하는 공통 인터페이스."""
    
    def __init__(self, base_url: str, name: str):
        """크롤러를 초기화합니다.
        
        Args:
            base_url: 크롤링 대상 사이트의 기본 URL
            name: 크롤러 이름
        """
        self.base_url = base_url
        self.name = name
    
    @abstractmethod
    async def crawl(self, **kwargs) -> List[Any]:
        """크롤링을 수행합니다.
        
        Args:
            **kwargs: 크롤링 옵션 (페이지 수, 날짜 범위 등)
            
        Returns:
            크롤링된 데이터 리스트
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """크롤러 상태를 확인합니다.
        
        Returns:
            크롤러가 정상 작동하면 True, 그렇지 않으면 False
        """
        pass


class CommunityCrawler(BaseCrawler):
    """커뮤니티 크롤러 기본 클래스."""
    
    @abstractmethod
    async def crawl_hot_posts(self, limit: int = 10) -> List[CrawledPost]:
        """인기 게시글을 크롤링합니다.
        
        Args:
            limit: 크롤링할 게시글 수
            
        Returns:
            크롤링된 게시글 리스트
        """
        pass
    
    @abstractmethod
    async def crawl_category(self, category: str, limit: int = 10) -> List[CrawledPost]:
        """특정 카테고리의 게시글을 크롤링합니다.
        
        Args:
            category: 크롤링할 카테고리
            limit: 크롤링할 게시글 수
            
        Returns:
            크롤링된 게시글 리스트
        """
        pass


class NewsCrawler(BaseCrawler):
    """뉴스 크롤러 기본 클래스."""
    
    @abstractmethod
    async def crawl_tech_news(self, limit: int = 10) -> List[NewsArticle]:
        """IT 뉴스를 크롤링합니다.
        
        Args:
            limit: 크롤링할 기사 수
            
        Returns:
            크롤링된 뉴스 기사 리스트
        """
        pass
    
    @abstractmethod
    async def crawl_telecom_news(self, limit: int = 10) -> List[NewsArticle]:
        """통신 뉴스를 크롤링합니다.
        
        Args:
            limit: 크롤링할 기사 수
            
        Returns:
            크롤링된 뉴스 기사 리스트
        """
        pass


class GovernmentCrawler(BaseCrawler):
    """정부 크롤러 기본 클래스."""
    
    @abstractmethod
    async def crawl_notices(self, limit: int = 10) -> List[GovernmentDocument]:
        """공지사항을 크롤링합니다.
        
        Args:
            limit: 크롤링할 문서 수
            
        Returns:
            크롤링된 정부 문서 리스트
        """
        pass
    
    @abstractmethod
    async def crawl_policies(self, limit: int = 10) -> List[GovernmentDocument]:
        """정책 자료를 크롤링합니다.
        
        Args:
            limit: 크롤링할 문서 수
            
        Returns:
            크롤링된 정부 문서 리스트
        """
        pass
