from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.newsletter import Newsletter, NewsletterCreate, NewsletterUpdate, NewsletterStatus
from app.services.newsletter_service import NewsletterService
from app.modules.newsletter.use_cases.daily_newsletter_use_case import DailyNewsletterUseCase

router = APIRouter()
newsletter_service = NewsletterService()


@router.post("/daily")
async def create_daily_newsletter(
    daily_use_case: DailyNewsletterUseCase = Depends()
):
    """일일 뉴스레터를 생성하고 발송합니다."""
    try:
        result = await daily_use_case.execute()
        return {
            "success": True,
            "message": "일일 뉴스레터가 성공적으로 생성되고 발송되었습니다.",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"뉴스레터 생성 실패: {str(e)}")


@router.post("/", response_model=Newsletter)
async def create_newsletter(newsletter_data: NewsletterCreate):
    """새 뉴스레터 생성"""
    try:
        newsletter = await newsletter_service.create_newsletter(newsletter_data)
        return newsletter
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Newsletter])
async def get_newsletters(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[NewsletterStatus] = None,
    search: Optional[str] = None
):
    """뉴스레터 목록 조회"""
    try:
        newsletters = await newsletter_service.get_newsletters(
            skip=skip, limit=limit, status=status, search=search
        )
        return newsletters
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{newsletter_id}", response_model=Newsletter)
async def get_newsletter(newsletter_id: PydanticObjectId):
    """특정 뉴스레터 조회"""
    try:
        newsletter = await newsletter_service.get_newsletter(newsletter_id)
        if not newsletter:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        return newsletter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{newsletter_id}", response_model=Newsletter)
async def update_newsletter(
    newsletter_id: PydanticObjectId,
    newsletter_data: NewsletterUpdate
):
    """뉴스레터 수정"""
    try:
        newsletter = await newsletter_service.update_newsletter(newsletter_id, newsletter_data)
        if not newsletter:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        return newsletter
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{newsletter_id}")
async def delete_newsletter(newsletter_id: PydanticObjectId):
    """뉴스레터 삭제"""
    try:
        success = await newsletter_service.delete_newsletter(newsletter_id)
        if not success:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        return {"message": "뉴스레터가 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{newsletter_id}/publish")
async def publish_newsletter(newsletter_id: PydanticObjectId):
    """뉴스레터 발행"""
    try:
        newsletter = await newsletter_service.publish_newsletter(newsletter_id)
        if not newsletter:
            raise HTTPException(status_code=404, detail="뉴스레터를 찾을 수 없습니다")
        return {"message": "뉴스레터가 발행되었습니다", "newsletter": newsletter}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
