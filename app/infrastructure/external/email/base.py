"""Base email service implementation."""

from __future__ import annotations

from abc import ABC
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.domain.ports import IEmailSender
from .interfaces import IEmailProvider, IEmailTemplateEngine, IEmailValidator, IEmailScheduler


class BaseEmailService(IEmailSender, IEmailProvider, IEmailTemplateEngine, IEmailValidator, IEmailScheduler, ABC):
    """Base implementation for email services with common functionality."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the email service."""
        if not self._initialized:
            await self._setup_provider()
            self._initialized = True
    
    async def _setup_provider(self) -> None:
        """Setup the underlying email provider."""
        # Override in subclasses
        pass
    
    # IEmailSender implementation
    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        """Send email using the provider."""
        return await self.send_bulk_email(recipients, subject, html_body)
    
    # IEmailTemplateEngine implementation
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render email template with context."""
        # Override in subclasses
        return f"Template: {template_name}"
    
    async def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template string with context."""
        # Override in subclasses
        return template_string
    
    async def validate_template(self, template_name: str) -> bool:
        """Validate template syntax."""
        # Override in subclasses
        return True
    
    # IEmailValidator implementation
    async def validate_email(self, email: str) -> bool:
        """Validate email address format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def validate_recipients(self, recipients: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Validate list of recipients."""
        validated = []
        for recipient in recipients:
            email = recipient.get("email", "")
            is_valid = await self.validate_email(email)
            validated.append({
                "email": email,
                "name": recipient.get("name", ""),
                "valid": is_valid
            })
        return validated
    
    async def check_deliverability(self, email: str) -> Dict[str, Any]:
        """Check email deliverability."""
        # Override in subclasses for advanced checking
        is_valid = await self.validate_email(email)
        return {
            "email": email,
            "valid": is_valid,
            "deliverable": is_valid,
            "reason": "Basic validation" if is_valid else "Invalid format"
        }
    
    # IEmailScheduler implementation
    async def schedule_email(self, email_data: Dict[str, Any], send_at: datetime) -> str:
        """Schedule email for future sending."""
        # Override in subclasses
        schedule_id = f"schedule_{datetime.utcnow().timestamp()}"
        return schedule_id
    
    async def cancel_scheduled_email(self, schedule_id: str) -> bool:
        """Cancel scheduled email."""
        # Override in subclasses
        return True
    
    async def get_scheduled_emails(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get scheduled emails in date range."""
        # Override in subclasses
        return []
    
    async def process_scheduled_emails(self) -> int:
        """Process and send scheduled emails."""
        # Override in subclasses
        return 0

