"""Email sender - 이메일 발송 전용."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailResult:
    """이메일 발송 결과."""
    recipient: str
    success: bool
    message_id: str
    sent_at: datetime


class EmailSender:
    """이메일 발송자 - 매우 직관적."""
    
    def __init__(self, email_service):
        self.email_service = email_service
    
    async def send_email(self, to: str, subject: str, content: str) -> EmailResult:
        """이메일을 발송합니다."""
        try:
            result = await self.email_service.send_email(to, subject, content)
            
            return EmailResult(
                recipient=to,
                success=True,
                message_id=result.get("message_id", "unknown"),
                sent_at=datetime.utcnow()
            )
        except Exception as e:
            return EmailResult(
                recipient=to,
                success=False,
                message_id="",
                sent_at=datetime.utcnow()
            )
    
    async def send_bulk_email(self, recipients: List[str], subject: str, content: str) -> List[EmailResult]:
        """대량 이메일을 발송합니다."""
        results = []
        
        for recipient in recipients:
            result = await self.send_email(recipient, subject, content)
            results.append(result)
        
        return results
