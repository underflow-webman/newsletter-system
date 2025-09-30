"""SMTP email service implementation."""

from __future__ import annotations

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from .base import BaseEmailService


class SMTPEmailService(BaseEmailService):
    """SMTP email service implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("smtp", config)
        self.smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = self.config.get("smtp_port", 587)
        self.username = self.config.get("username")
        self.password = self.config.get("password")
        self.from_email = self.config.get("from_email")
        self.from_name = self.config.get("from_name", "Newsletter System")
        self._server = None
    
    async def _setup_provider(self) -> None:
        """Setup SMTP connection."""
        if not all([self.username, self.password, self.from_email]):
            raise ValueError("SMTP credentials are required")
    
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send single email via SMTP."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send bulk emails via SMTP."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            
            # Add HTML content
            html_part = MIMEText(body, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Add text content if provided
            text_content = kwargs.get("text_content")
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # Connect to SMTP server
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                
                # Send to each recipient
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
        """SMTP doesn't provide delivery status tracking."""
        return {
            "message_id": message_id,
            "status": "unknown",
            "delivered_at": None,
            "error": "SMTP doesn't provide delivery status"
        }

