"""SMTP 이메일 서비스 구현."""

from __future__ import annotations

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from .base import BaseEmailService


class SMTPEmailService(BaseEmailService):
    """SMTP 이메일 서비스 구현."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """SMTP 이메일 서비스를 초기화합니다."""
        super().__init__("smtp", config)
        self.smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.username = self.config.get("username")
        self.password = self.config.get("password")
        self.from_email = self.config.get("from_email")
        self.from_name = self.config.get("from_name", "Newsletter System")
        self._server = None
    
    async def _setup_provider(self) -> None:
        """SMTP 연결을 설정합니다."""
        if not all([self.username, self.password, self.from_email]):
            raise ValueError("SMTP credentials are required")
    
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """SMTP를 통해 단일 이메일을 발송합니다."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """SMTP를 통해 대량 이메일을 발송합니다."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # 메시지 생성
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            
            # HTML 콘텐츠 추가
            html_part = MIMEText(body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 텍스트 콘텐츠가 제공된 경우 추가
            text_content = kwargs.get("text_content")
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # SMTP 서버에 연결
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                
                # 각 수신자에게 발송
                sent_count = 0
                for recipient in recipients:
                    msg['To'] = recipient["email"]
                    server.send_message(msg)
                    sent_count += 1
            
            return {
                "status": "success",
                "sent_count": sent_count,
                "total_recipients": len(recipients)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "sent_count": 0
            }
    
    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """SMTP는 배송 상태 추적을 제공하지 않습니다."""
        return {
            "message_id": message_id,
            "status": "unknown",
            "delivered_at": None,
            "error": "SMTP doesn't provide delivery status"
        }

