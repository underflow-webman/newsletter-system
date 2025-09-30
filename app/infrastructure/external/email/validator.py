"""Email validation implementations."""

from __future__ import annotations

import re
import dns.resolver
from typing import List, Dict, Any, Optional
from .interfaces import IEmailValidator


class EmailValidator(IEmailValidator):
    """Email validation service."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.check_mx = self.config.get("check_mx", False)
        self.check_smtp = self.config.get("check_smtp", False)
    
    async def validate_email(self, email: str) -> bool:
        """Validate email address format."""
        if not email or not isinstance(email, str):
            return False
        
        # Basic format validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False
        
        # Additional checks if enabled
        if self.check_mx:
            if not await self._check_mx_record(email):
                return False
        
        if self.check_smtp:
            if not await self._check_smtp_validation(email):
                return False
        
        return True
    
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
        is_valid = await self.validate_email(email)
        
        if not is_valid:
            return {
                "email": email,
                "valid": False,
                "deliverable": False,
                "reason": "Invalid email format"
            }
        
        # Check MX record
        mx_valid = await self._check_mx_record(email)
        
        return {
            "email": email,
            "valid": is_valid,
            "deliverable": mx_valid,
            "reason": "MX record check" if mx_valid else "No MX record found"
        }
    
    async def _check_mx_record(self, email: str) -> bool:
        """Check if domain has MX record."""
        try:
            domain = email.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except Exception:
            return False
    
    async def _check_smtp_validation(self, email: str) -> bool:
        """Check SMTP validation (simplified)."""
        # This is a simplified implementation
        # In production, you might want to use a service like ZeroBounce or Hunter
        try:
            domain = email.split('@')[1]
            # Basic domain existence check
            dns.resolver.resolve(domain, 'A')
            return True
        except Exception:
            return False

