import httpx
import json
from typing import Dict, List, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DaouOfficeService:
    def __init__(self):
        self.api_url = settings.DAOU_OFFICE_API_URL
        self.api_key = settings.DAOU_OFFICE_API_KEY
        self.secret = settings.DAOU_OFFICE_SECRET
        self.from_email = settings.FROM_EMAIL
        self.from_name = settings.FROM_NAME

    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[Dict]] = None
    ) -> Dict:
        """
        다우오피스 API를 통해 이메일 발송
        
        Args:
            to_emails: 수신자 이메일 리스트
            subject: 이메일 제목
            html_content: HTML 내용
            text_content: 텍스트 내용 (선택사항)
            attachments: 첨부파일 리스트 (선택사항)
        
        Returns:
            발송 결과 딕셔너리
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "from": {
                    "email": self.from_email,
                    "name": self.from_name
                },
                "to": [{"email": email} for email in to_emails],
                "subject": subject,
                "html": html_content,
                "text": text_content or self._html_to_text(html_content)
            }
            
            if attachments:
                payload["attachments"] = attachments
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/send",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"이메일 발송 성공: {len(to_emails)}명에게 발송")
                    return {
                        "success": True,
                        "message_id": result.get("message_id"),
                        "recipients": len(to_emails),
                        "response": result
                    }
                else:
                    logger.error(f"이메일 발송 실패: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"API Error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"이메일 발송 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def send_bulk_email(
        self,
        recipients: List[Dict],  # [{"email": "test@example.com", "name": "홍길동"}]
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> Dict:
        """
        대량 이메일 발송 (개인화 가능)
        
        Args:
            recipients: 수신자 정보 리스트
            subject: 이메일 제목
            html_content: HTML 내용 (개인화 변수 포함 가능)
            text_content: 텍스트 내용
        
        Returns:
            발송 결과 딕셔너리
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 개인화된 이메일 데이터 생성
            personalizations = []
            for recipient in recipients:
                personalizations.append({
                    "to": [{"email": recipient["email"], "name": recipient.get("name", "")}],
                    "subject": subject,
                    "substitutions": {
                        "{{name}}": recipient.get("name", ""),
                        "{{email}}": recipient["email"]
                    }
                })
            
            payload = {
                "from": {
                    "email": self.from_email,
                    "name": self.from_name
                },
                "personalizations": personalizations,
                "subject": subject,
                "html": html_content,
                "text": text_content or self._html_to_text(html_content)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/send/bulk",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"대량 이메일 발송 성공: {len(recipients)}명에게 발송")
                    return {
                        "success": True,
                        "message_id": result.get("message_id"),
                        "recipients": len(recipients),
                        "response": result
                    }
                else:
                    logger.error(f"대량 이메일 발송 실패: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"API Error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"대량 이메일 발송 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_delivery_status(self, message_id: str) -> Dict:
        """
        이메일 발송 상태 확인
        
        Args:
            message_id: 발송된 이메일의 메시지 ID
        
        Returns:
            발송 상태 정보
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/status/{message_id}",
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "status": response.json()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API Error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"발송 상태 확인 중 오류 발생: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _html_to_text(self, html_content: str) -> str:
        """
        HTML을 텍스트로 변환 (간단한 구현)
        """
        import re
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', html_content)
        # 여러 공백을 하나로
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    async def validate_email(self, email: str) -> bool:
        """
        이메일 주소 유효성 검사
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/validate",
                    headers=headers,
                    json={"email": email},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("valid", False)
                return False
                
        except Exception as e:
            logger.error(f"이메일 유효성 검사 중 오류: {str(e)}")
            return False


# 싱글톤 인스턴스
daou_office_service = DaouOfficeService()
