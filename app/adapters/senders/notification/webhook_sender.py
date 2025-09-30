"""Webhook sender - 웹훅 발송자."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebhookResult:
    """웹훅 발송 결과."""
    url: str
    success: bool
    status_code: int
    sent_at: datetime


class WebhookSender:
    """웹훅 발송자."""
    
    def __init__(self, http_client):
        self.http_client = http_client
    
    async def send_webhook(self, url: str, data: Dict[str, Any]) -> WebhookResult:
        """웹훅을 발송합니다."""
        try:
            response = await self.http_client.post(url, json=data)
            
            return WebhookResult(
                url=url,
                success=response.status_code == 200,
                status_code=response.status_code,
                sent_at=datetime.utcnow()
            )
        except Exception as e:
            return WebhookResult(
                url=url,
                success=False,
                status_code=0,
                sent_at=datetime.utcnow()
            )
