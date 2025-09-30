"""Slack sender - 슬랙 발송자."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SlackResult:
    """슬랙 발송 결과."""
    channel: str
    success: bool
    message_id: str
    sent_at: datetime


class SlackSender:
    """슬랙 발송자."""
    
    def __init__(self, slack_client):
        self.slack_client = slack_client
    
    async def send_message(self, channel: str, message: str) -> SlackResult:
        """슬랙 메시지를 발송합니다."""
        try:
            result = await self.slack_client.send_message(channel, message)
            
            return SlackResult(
                channel=channel,
                success=True,
                message_id=result.get("ts", "unknown"),
                sent_at=datetime.utcnow()
            )
        except Exception as e:
            return SlackResult(
                channel=channel,
                success=False,
                message_id="",
                sent_at=datetime.utcnow()
            )
