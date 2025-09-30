"""뉴스레터 서비스들 - 뉴스레터 비즈니스 로직을 담당하는 서비스 계층."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import Newsletter, NewsletterItem, Subscriber
from .repositories import NewsletterRepository, SubscriberRepository


class NewsletterService:
    """뉴스레터 서비스 - 뉴스레터 관련 비즈니스 로직을 처리합니다."""
    
    def __init__(self, newsletter_repo: NewsletterRepository, subscriber_repo: SubscriberRepository):
        self.newsletter_repo = newsletter_repo
        self.subscriber_repo = subscriber_repo
    
    async def create_newsletter(self, items: List[NewsletterItem], title: str) -> Newsletter:
        """뉴스레터를 생성합니다."""
        newsletter = Newsletter(
            id=f"newsletter_{datetime.utcnow().timestamp()}",
            title=title,
            items=items,
            status="draft",
            scheduled_at=None,
            sent_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        await self.newsletter_repo.save(newsletter)
        return newsletter
    
    async def get_newsletter(self, newsletter_id: str) -> Newsletter:
        """뉴스레터를 조회합니다."""
        return await self.newsletter_repo.get_by_id(newsletter_id)
    
    async def list_newsletters(self, status: str = None) -> List[Newsletter]:
        """뉴스레터 목록을 조회합니다."""
        if status:
            return await self.newsletter_repo.list_by_status(status)
        return await self.newsletter_repo.list_by_status("all")


class TemplateService:
    """템플릿 서비스 - 뉴스레터 HTML 템플릿을 렌더링합니다."""
    
    async def render_newsletter_template(self, newsletter: Newsletter) -> str:
        """뉴스레터 템플릿을 HTML로 렌더링합니다."""
        # TODO: 실제 템플릿 엔진을 사용한 렌더링 로직 구현
        html = f"""
        <html>
        <body>
            <h1>{newsletter.title}</h1>
            <p>총 {len(newsletter.items)}개의 뉴스가 있습니다.</p>
            <ul>
        """
        
        for item in newsletter.items:
            html += f"""
                <li>
                    <h3>{item.title}</h3>
                    <p>{item.content[:100]}...</p>
                    <a href="{item.url}">자세히 보기</a>
                </li>
            """
        
        html += """
            </ul>
        </body>
        </html>
        """
        
        return html
