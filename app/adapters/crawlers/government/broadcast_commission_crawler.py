"""Broadcast Commission crawler - 방송통신위원회 크롤러."""

from __future__ import annotations

from typing import List
from app.modules.crawling.entities import GovernmentDocument


class BroadcastCommissionCrawler:
    """방송통신위원회 크롤러."""
    
    def __init__(self):
        self.base_url = "https://www.kcc.go.kr"
        self.name = "broadcast_commission"
    
    async def crawl_notices(self) -> List[GovernmentDocument]:
        """공지사항을 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
    
    async def crawl_policies(self) -> List[GovernmentDocument]:
        """정책 자료를 크롤링합니다."""
        # TODO: 실제 크롤링 로직 구현
        return []
