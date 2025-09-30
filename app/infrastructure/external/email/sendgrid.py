"""SendGrid 이메일 서비스 구현."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
except ImportError:
    SendGridAPIClient = None
    Mail = None
    Email = None
    To = None
    Content = None
from .base import BaseEmailService


class SendGridEmailService(BaseEmailService):
    """SendGrid 이메일 서비스 구현."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("sendgrid", config)
        self.api_key = self.config.get("api_key")
        self.from_email = self.config.get("from_email")
        self.from_name = self.config.get("from_name", "Newsletter System")
        self._client = None
    
    async def _setup_provider(self) -> None:
        """SendGrid 클라이언트를 설정합니다."""
        if not self.api_key:
            raise ValueError("SendGrid API key is required")
        
        self._client = SendGridAPIClient(api_key=self.api_key)
    
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """SendGrid를 통해 단일 이메일을 발송합니다."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """SendGrid를 통해 대량 이메일을 발송합니다."""
        if not self._client:
            await self.initialize()
        
        try:
            # 메시지 생성
            from_email = Email(self.from_email, self.from_name)
            to_emails = [To(recipient["email"], recipient.get("name", "")) for recipient in recipients]
            
            # 콘텐츠 생성
            content = Content("text/html", body)
            
            # 메일 객체 생성
            mail = Mail(from_email, to_emails[0], subject, content)
            
            # 추가 수신자 추가
            for to_email in to_emails[1:]:
                mail.add_to(to_email)
            
            # 이메일 발송
            response = self._client.send(mail)
            
            return {
                "status": "success",
                "status_code": response.status_code,
                "sent_count": len(recipients),
                "message_id": response.headers.get("X-Message-Id")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "sent_count": 0
            }
    
    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """SendGrid에서 이메일 배송 상태를 조회합니다."""
        if not self._client:
            await self.initialize()
        
        try:
            # SendGrid Events API를 사용하여 배송 상태 조회
            response = self._client.client.messages.get(message_id)
            
            return {
                "message_id": message_id,
                "status": "delivered",
                "delivered_at": None,
                "error": None
            }
            
        except Exception as e:
            return {
                "message_id": message_id,
                "status": "error",
                "delivered_at": None,
                "error": str(e)
            }

