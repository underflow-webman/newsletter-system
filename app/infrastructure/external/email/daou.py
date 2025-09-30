"""다우오피스 이메일 서비스 구현."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from .base import BaseEmailService


class DaouEmailSenderAdapter(BaseEmailService):
    """다우오피스 이메일 서비스 어댑터."""
    
    def __init__(self, daou_service, config: Optional[Dict[str, Any]] = None):
        super().__init__("daou", config)
        self._daou_service = daou_service
    
    # IEmailSender 구현
    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        """다우오피스 서비스를 사용하여 이메일을 발송합니다."""
        return await self._daou_service.send_bulk_email(
            recipients=recipients,
            subject=subject,
            html_content=html_body,
            text_content="",
        )
    
    # IEmailProvider 구현
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """다우오피스를 사용하여 단일 이메일을 발송합니다."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """다우오피스를 사용하여 대량 이메일을 발송합니다."""
        return await self._daou_service.send_bulk_email(
            recipients=recipients,
            subject=subject,
            html_content=body,
            text_content=kwargs.get("text_content", ""),
        )
    
    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """다우오피스에서 이메일 배송 상태를 조회합니다."""
        # 실제 다우오피스 API 호출로 오버라이드
        return {
            "message_id": message_id,
            "status": "delivered",
            "delivered_at": None,
            "error": None
        }

