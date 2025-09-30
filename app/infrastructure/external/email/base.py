"""기본 이메일 서비스 구현."""

from __future__ import annotations

from abc import ABC
from typing import List, Dict, Any, Optional
from datetime import datetime
from .interfaces import IEmailProvider, IEmailTemplateEngine, IEmailValidator, IEmailScheduler


class BaseEmailService(IEmailProvider, IEmailTemplateEngine, IEmailValidator, IEmailScheduler, ABC):
    """공통 기능을 가진 이메일 서비스의 기본 구현."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """이메일 서비스를 초기화합니다."""
        if not self._initialized:
            await self._setup_provider()
            self._initialized = True
    
    async def _setup_provider(self) -> None:
        """기본 이메일 제공자를 설정합니다."""
        # 서브클래스에서 오버라이드
        pass
    
    # IEmailSender 구현
    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        """제공자를 사용하여 이메일을 발송합니다."""
        return await self.send_bulk_email(recipients, subject, html_body)
    
    # IEmailTemplateEngine 구현
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """컨텍스트와 함께 이메일 템플릿을 렌더링합니다."""
        # 서브클래스에서 오버라이드
        return f"Template: {template_name}"
    
    async def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """컨텍스트와 함께 템플릿 문자열을 렌더링합니다."""
        # 서브클래스에서 오버라이드
        return template_string
    
    async def validate_template(self, template_name: str) -> bool:
        """템플릿 구문을 검증합니다."""
        # 서브클래스에서 오버라이드
        return True
    
    # IEmailValidator 구현
    async def validate_email(self, email: str) -> bool:
        """이메일 주소 형식을 검증합니다."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
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
        # 고급 검사를 위해 서브클래스에서 오버라이드
        is_valid = await self.validate_email(email)
        return {
            "email": email,
            "valid": is_valid,
            "deliverable": is_valid,
            "reason": "Basic validation" if is_valid else "Invalid format"
        }
    
    # IEmailScheduler 구현
    async def schedule_email(self, email_data: Dict[str, Any], send_at: datetime) -> str:
        """나중에 발송할 이메일을 예약합니다."""
        # 서브클래스에서 오버라이드
        schedule_id = f"schedule_{datetime.utcnow().timestamp()}"
        return schedule_id
    
    async def cancel_scheduled_email(self, schedule_id: str) -> bool:
        """예약된 이메일을 취소합니다."""
        # 서브클래스에서 오버라이드
        return True
    
    async def get_scheduled_emails(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """날짜 범위 내의 예약된 이메일을 조회합니다."""
        # 서브클래스에서 오버라이드
        return []
    
    async def process_scheduled_emails(self) -> int:
        """예약된 이메일을 처리하고 발송합니다."""
        # 서브클래스에서 오버라이드
        return 0

