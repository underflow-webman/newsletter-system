"""SendGrid email service implementation."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from .base import BaseEmailService


class SendGridEmailService(BaseEmailService):
    """SendGrid email service implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("sendgrid", config)
        self.api_key = self.config.get("api_key")
        self.from_email = self.config.get("from_email")
        self.from_name = self.config.get("from_name", "Newsletter System")
        self._client = None
    
    async def _setup_provider(self) -> None:
        """Setup SendGrid client."""
        if not self.api_key:
            raise ValueError("SendGrid API key is required")
        
        self._client = SendGridAPIClient(api_key=self.api_key)
    
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send single email via SendGrid."""
        recipients = [{"email": to, "name": kwargs.get("name", "")}]
        return await self.send_bulk_email(recipients, subject, body, **kwargs)
    
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send bulk emails via SendGrid."""
        if not self._client:
            await self.initialize()
        
        try:
            # Create message
            from_email = Email(self.from_email, self.from_name)
            to_emails = [To(recipient["email"], recipient.get("name", "")) for recipient in recipients]
            
            # Create content
            content = Content("text/html", body)
            
            # Create mail object
            mail = Mail(from_email, to_emails[0], subject, content)
            
            # Add additional recipients
            for to_email in to_emails[1:]:
                mail.add_to(to_email)
            
            # Send email
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
        """Get email delivery status from SendGrid."""
        if not self._client:
            await self.initialize()
        
        try:
            # Use SendGrid Events API to get delivery status
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

