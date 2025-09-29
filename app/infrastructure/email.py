from __future__ import annotations

from typing import List, Dict

from app.domain.ports import IEmailSender


class DaouEmailSenderAdapter(IEmailSender):
    """도메인 포트(IEmailSender)를 다우오피스 서비스로 연결하는 어댑터."""

    def __init__(self, daou_service) -> None:
        self._svc = daou_service

    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        return await self._svc.send_bulk_email(
            recipients=recipients,
            subject=subject,
            html_content=html_body,
            text_content="",
        )


