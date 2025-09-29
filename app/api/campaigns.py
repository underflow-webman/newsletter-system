from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStats, CampaignStatus
from app.services.campaign_service import CampaignService

router = APIRouter()
campaign_service = CampaignService()


@router.post("/", response_model=Campaign)
async def create_campaign(campaign_data: CampaignCreate):
    """새 캠페인 생성"""
    try:
        campaign = await campaign_service.create_campaign(campaign_data)
        return campaign
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Campaign])
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[CampaignStatus] = None,
    search: Optional[str] = None
):
    """캠페인 목록 조회"""
    try:
        campaigns = await campaign_service.get_campaigns(
            skip=skip, limit=limit, status=status, search=search
        )
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: PydanticObjectId):
    """특정 캠페인 조회"""
    try:
        campaign = await campaign_service.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: PydanticObjectId,
    campaign_data: CampaignUpdate
):
    """캠페인 수정"""
    try:
        campaign = await campaign_service.update_campaign(campaign_id, campaign_data)
        if not campaign:
            raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")
        return campaign
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: PydanticObjectId):
    """캠페인 삭제"""
    try:
        success = await campaign_service.delete_campaign(campaign_id)
        if not success:
            raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")
        return {"message": "캠페인이 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/send")
async def send_campaign(campaign_id: PydanticObjectId):
    """캠페인 발송"""
    try:
        result = await campaign_service.send_campaign(campaign_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/schedule")
async def schedule_campaign(
    campaign_id: PydanticObjectId,
    scheduled_at: str  # ISO datetime string
):
    """캠페인 예약 발송"""
    try:
        result = await campaign_service.schedule_campaign(campaign_id, scheduled_at)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
async def get_campaign_stats(campaign_id: PydanticObjectId):
    """캠페인 통계 조회"""
    try:
        stats = await campaign_service.get_campaign_stats(campaign_id)
        if not stats:
            raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
