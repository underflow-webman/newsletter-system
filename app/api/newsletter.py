"""뉴스레터 API 엔드포인트 - 뉴스레터 관련 REST API."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId

from app.modules.newsletter.entities import Newsletter, NewsletterItem, Subscriber
from app.modules.newsletter.services import NewsletterService, TemplateService
from app.modules.newsletter.use_cases import DailyNewsletterUseCase
from app.infrastructure.di import get_dependency_container

router = APIRouter()


@router.post("/daily")
async def create_daily_newsletter() -> Dict[str, Any]:
    """일일 뉴스레터를 생성하고 발송합니다."""
    try:
        container = get_dependency_container()
        daily_use_case = container.get_daily_newsletter_use_case()
        result = await daily_use_case.execute()
        
        return {
            "success": True,
            "message": "일일 뉴스레터가 성공적으로 생성되고 발송되었습니다.",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"뉴스레터 생성 실패: {str(e)}")


@router.get("/")
async def get_newsletters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None
):
    """뉴스레터 목록을 조회합니다."""
    try:
        container = get_dependency_container()
        newsletter_service = container.get_newsletter_service()
        newsletters = await newsletter_service.list_newsletters(status=status)
        return newsletters[skip:skip + limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{newsletter_id}")
async def get_newsletter(newsletter_id: str):
    """특정 뉴스레터를 조회합니다."""
    try:
        container = get_dependency_container()
        newsletter_service = container.get_newsletter_service()
        newsletter = await newsletter_service.get_newsletter(newsletter_id)
        if not newsletter:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        return newsletter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{newsletter_id}/send")
async def send_newsletter(newsletter_id: str) -> Dict[str, Any]:
    """뉴스레터를 발송합니다."""
    try:
        container = get_dependency_container()
        newsletter_service = container.get_newsletter_service()
        template_service = container.get_template_service()
        email_service = container.get_email_service()
        
        # 뉴스레터 조회
        newsletter = await newsletter_service.get_newsletter(newsletter_id)
        if not newsletter:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        
        # HTML 템플릿 렌더링
        html_content = await template_service.render_newsletter_template(newsletter)
        
        # 이메일 발송 (임시 구독자 목록)
        recipients = [{"email": "test@example.com", "name": "Test User"}]
        result = await email_service.send_bulk_email(
            recipients=recipients,
            subject=newsletter.title,
            body=html_content
        )
        
        return {
            "success": True,
            "message": "뉴스레터가 성공적으로 발송되었습니다.",
            "send_result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
