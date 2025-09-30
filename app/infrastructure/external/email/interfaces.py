"""Email service interfaces for different capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.domain.ports import IEmailSender


class IEmailProvider(ABC):
    """Base interface for email providers."""
    
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send single email."""
        pass
    
    @abstractmethod
    async def send_bulk_email(self, recipients: List[Dict[str, str]], subject: str, body: str, **kwargs) -> Dict[str, Any]:
        """Send bulk emails."""
        pass
    
    @abstractmethod
    async def get_delivery_status(self, message_id: str) -> Dict[str, Any]:
        """Get email delivery status."""
        pass


class IEmailTemplateEngine(ABC):
    """Interface for email template engines."""
    
    @abstractmethod
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render email template with context."""
        pass
    
    @abstractmethod
    async def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template string with context."""
        pass
    
    @abstractmethod
    async def validate_template(self, template_name: str) -> bool:
        """Validate template syntax."""
        pass


class IEmailValidator(ABC):
    """Interface for email validation."""
    
    @abstractmethod
    async def validate_email(self, email: str) -> bool:
        """Validate email address format."""
        pass
    
    @abstractmethod
    async def validate_recipients(self, recipients: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Validate list of recipients."""
        pass
    
    @abstractmethod
    async def check_deliverability(self, email: str) -> Dict[str, Any]:
        """Check email deliverability."""
        pass


class IEmailScheduler(ABC):
    """Interface for email scheduling."""
    
    @abstractmethod
    async def schedule_email(self, email_data: Dict[str, Any], send_at: datetime) -> str:
        """Schedule email for future sending."""
        pass
    
    @abstractmethod
    async def cancel_scheduled_email(self, schedule_id: str) -> bool:
        """Cancel scheduled email."""
        pass
    
    @abstractmethod
    async def get_scheduled_emails(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get scheduled emails in date range."""
        pass
    
    @abstractmethod
    async def process_scheduled_emails(self) -> int:
        """Process and send scheduled emails."""
        pass


class IAdvancedEmailService(IEmailSender, ABC):
    """Advanced email service with additional capabilities."""
    
    @abstractmethod
    async def send_with_template(self, template_name: str, recipients: List[Dict[str, str]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Send email using template."""
        pass
    
    @abstractmethod
    async def send_with_attachments(self, recipients: List[Dict[str, str]], subject: str, body: str, attachments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send email with attachments."""
        pass
    
    @abstractmethod
    async def track_email_opens(self, message_id: str) -> Dict[str, Any]:
        """Track email open events."""
        pass
    
    @abstractmethod
    async def track_email_clicks(self, message_id: str) -> Dict[str, Any]:
        """Track email click events."""
        pass

