"""KAIT crawler - 한국정보통신기술협회 크롤러."""

from __future__ import annotations

from typing import List
from datetime import datetime
from dataclasses import dataclass


@dataclass
class GovernmentDocument:
    """정부 문서."""
    title: str
    content: str
    url: str
    department: str
    published_at: datetime
    document_type: str


class KaitCrawler:
    """한국정보통신기술협회 크롤러."""
    
    def __init__(self):
        self.base_url = "https://www.kait.or.kr"
        self.name = "kait"
    
    async def crawl_notices(self) -> List[GovernmentDocument]:
        """공지사항을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
    
    async def crawl_reports(self) -> List[GovernmentDocument]:
        """보고서를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
