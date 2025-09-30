"""이메일 검증 구현."""

from __future__ import annotations

import re
import dns.resolver
from typing import List, Dict, Any, Optional
from .interfaces import IEmailValidator


class EmailValidator(IEmailValidator):
    """이메일 검증 서비스."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """이메일 검증 서비스를 초기화합니다."""
        self.config = config or {}
        self.check_mx = self.config.get("check_mx", False)
        self.check_smtp = self.config.get("check_smtp", False)
    
    async def validate_email(self, email: str) -> bool:
        """이메일 주소 형식을 검증합니다."""
        if not email or not isinstance(email, str):
            return False
        
        # 기본 형식 검증
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False
        
        # 활성화된 경우 추가 검사
        if self.check_mx:
            if not await self._check_mx_record(email):
                return False
        
        if self.check_smtp:
            if not await self._check_smtp_validation(email):
                return False
        
        return True
    
    async def validate_recipients(self, recipients: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """수신자 목록을 검증합니다."""
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
        """이메일 전달 가능성을 확인합니다."""
        is_valid = await self.validate_email(email)
        
        if not is_valid:
            return {
                "email": email,
                "valid": False,
                "deliverable": False,
                "reason": "Invalid email format"
            }
        
        # MX 레코드 확인
        mx_valid = await self._check_mx_record(email)
        
        return {
            "email": email,
            "valid": is_valid,
            "deliverable": mx_valid,
            "reason": "MX record check" if mx_valid else "No MX record found"
        }
    
    async def _check_mx_record(self, email: str) -> bool:
        """도메인에 MX 레코드가 있는지 확인합니다."""
        try:
            domain = email.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
            return len(mx_records) > 0
        except Exception:
            return False
    
    async def _check_smtp_validation(self, email: str) -> bool:
        """SMTP 검증을 확인합니다 (간소화된 버전)."""
        # 이는 간소화된 구현입니다
        # 프로덕션에서는 ZeroBounce나 Hunter 같은 서비스를 사용하는 것이 좋습니다
        try:
            domain = email.split('@')[1]
            # 기본 도메인 존재 확인
            dns.resolver.resolve(domain, 'A')
            return True
        except Exception:
            return False

