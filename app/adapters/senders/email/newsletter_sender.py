"""Newsletter sender - 뉴스레터 발송 전용."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsletterItem:
    """뉴스레터 아이템."""
    title: str
    content: str
    source: str
    url: str
    category: str
    created_at: datetime


@dataclass
class NewsletterResult:
    """뉴스레터 발송 결과."""
    recipient: str
    success: bool
    message_id: str
    sent_at: datetime


class NewsletterSender:
    """뉴스레터 발송자 - 매우 직관적."""
    
    def __init__(self, email_sender, template_service):
        self.email_sender = email_sender
        self.template_service = template_service
    
    async def send_newsletter(self, recipients: List[str], items: List[NewsletterItem]) -> List[NewsletterResult]:
        """뉴스레터를 발송합니다."""
        # 뉴스레터 HTML 생성
        html_content = await self._create_newsletter_html(items)
        
        # 이메일 발송
        subject = f"일일 뉴스레터 - {datetime.utcnow().strftime('%Y-%m-%d')}"
        results = await self.email_sender.send_bulk_email(recipients, subject, html_content)
        
        return results
    
    async def _create_newsletter_html(self, items: List[NewsletterItem]) -> str:
        """뉴스레터 HTML을 생성합니다."""
        # TODO: 실제 HTML 템플릿 생성
        html = f"""
        <html>
        <body>
            <h1>일일 뉴스레터</h1>
            <p>총 {len(items)}개의 뉴스가 있습니다.</p>
        </body>
        </html>
        """
        return html
