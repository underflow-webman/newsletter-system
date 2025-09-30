"""Newsletter use cases - 뉴스레터 유즈케이스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import Newsletter, NewsletterItem
from .services import NewsletterService, TemplateService
from .repositories import NewsletterRepository, SubscriberRepository


class CreateNewsletterUseCase:
    """뉴스레터 생성 유즈케이스."""
    
    def __init__(self, newsletter_service: NewsletterService):
        self.newsletter_service = newsletter_service
    
    async def execute(self, items: List[Dict[str, Any]], title: str) -> Newsletter:
        """뉴스레터를 생성합니다."""
        # 데이터를 NewsletterItem으로 변환
        newsletter_items = [
            NewsletterItem(
                id=f"item_{i}",
                title=item["title"],
                content=item["content"],
                source=item["source"],
                url=item["url"],
                category=item.get("category", "general"),
                relevance_score=item.get("relevance_score", 0.0),
                created_at=datetime.utcnow()
            )
            for i, item in enumerate(items)
        ]
        
        return await self.newsletter_service.create_newsletter(newsletter_items, title)


class SendNewsletterUseCase:
    """뉴스레터 발송 유즈케이스."""
    
    def __init__(self, newsletter_service: NewsletterService, template_service: TemplateService, email_sender):
        self.newsletter_service = newsletter_service
        self.template_service = template_service
        self.email_sender = email_sender
    
    async def execute(self, newsletter_id: str, recipients: List[str]) -> Dict[str, Any]:
        """뉴스레터를 발송합니다."""
        # 뉴스레터 조회
        newsletter = await self.newsletter_service.get_newsletter(newsletter_id)
        if not newsletter:
            raise ValueError(f"Newsletter {newsletter_id} not found")
        
        # 템플릿 렌더링
        html_content = await self.template_service.render_newsletter_template(newsletter)
        
        # 이메일 발송
        results = []
        for recipient in recipients:
            try:
                result = await self.email_sender.send_email(
                    to=recipient,
                    subject=newsletter.title,
                    content=html_content
                )
                results.append({
                    "recipient": recipient,
                    "success": True,
                    "message_id": result.get("message_id")
                })
            except Exception as e:
                results.append({
                    "recipient": recipient,
                    "success": False,
                    "error": str(e)
                })
        
        # 상태 업데이트
        await self.newsletter_service.newsletter_repo.update_status(newsletter_id, "sent")
        
        return {
            "newsletter_id": newsletter_id,
            "total_recipients": len(recipients),
            "successful_sends": sum(1 for r in results if r["success"]),
            "failed_sends": sum(1 for r in results if not r["success"]),
            "results": results
        }
