"""Daou Office email service implementation."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from app.domain.ports import IEmailSender
from .base import BaseEmailService


class DaouEmailSenderAdapter(BaseEmailService):
    """Daou Office email service adapter."""
    
    def __init__(self, daou_service, config: Optional[Dict[str, Any]] = None):
        super().__init__("daou", config)
        self._daou_service = daou_service
    
    # IEmailSender implementation
    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        """Send email using Daou Office service."""
        return await self._daou_service.send_bulk_email(
            recipients=recipients,
            subject=subject,
            html_content=html_body,
            text_content="",
        )
    
    # IEmailProvider implementation
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send single email using Daou Office."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send bulk emails using Daou Office."""
        return await self._daou_service.send_bulk_email(
            recipients=recipients,
            subject=subject,
            html_content=body,
            text_content=kwargs.get("text_content", ""),
        )
    
    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """Get email delivery status from Daou Office."""
        # Override with actual Daou Office API call
        return {
            "message_id": message_id,
            "status": "delivered",
            "delivered_at": None,
            "error": None
        }

