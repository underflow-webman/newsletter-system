from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from beanie import PydanticObjectId

from app.models.subscriber import Subscriber, SubscriberCreate, SubscriberUpdate, SubscriberBulkImport, SubscriptionStatus
from app.services.subscriber_service import SubscriberService

router = APIRouter()
subscriber_service = SubscriberService()


@router.post("/", response_model=Subscriber)
async def create_subscriber(subscriber_data: SubscriberCreate):
    """새 구독자 추가"""
    try:
        subscriber = await subscriber_service.create_subscriber(subscriber_data)
        return subscriber
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk", response_model=dict)
async def bulk_import_subscribers(import_data: SubscriberBulkImport):
    """구독자 대량 등록"""
    try:
        result = await subscriber_service.bulk_import_subscribers(import_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Subscriber])
async def get_subscribers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[SubscriptionStatus] = None,
    search: Optional[str] = None
):
    """구독자 목록 조회"""
    try:
        subscribers = await subscriber_service.get_subscribers(
            skip=skip, limit=limit, status=status, search=search
        )
        return subscribers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{subscriber_id}", response_model=Subscriber)
async def get_subscriber(subscriber_id: PydanticObjectId):
    """특정 구독자 조회"""
    try:
        subscriber = await subscriber_service.get_subscriber(subscriber_id)
        if not subscriber:
            raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")
        return subscriber
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{subscriber_id}", response_model=Subscriber)
async def update_subscriber(
    subscriber_id: PydanticObjectId,
    subscriber_data: SubscriberUpdate
):
    """구독자 정보 수정"""
    try:
        subscriber = await subscriber_service.update_subscriber(subscriber_id, subscriber_data)
        if not subscriber:
            raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")
        return subscriber
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{subscriber_id}")
async def delete_subscriber(subscriber_id: PydanticObjectId):
    """구독자 삭제"""
    try:
        success = await subscriber_service.delete_subscriber(subscriber_id)
        if not success:
            raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")
        return {"message": "구독자가 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{subscriber_id}/unsubscribe")
async def unsubscribe_subscriber(subscriber_id: PydanticObjectId):
    """구독 해지"""
    try:
        subscriber = await subscriber_service.unsubscribe_subscriber(subscriber_id)
        if not subscriber:
            raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")
        return {"message": "구독이 해지되었습니다", "subscriber": subscriber}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email/{email}", response_model=Subscriber)
async def get_subscriber_by_email(email: str):
    """이메일로 구독자 조회"""
    try:
        subscriber = await subscriber_service.get_subscriber_by_email(email)
        if not subscriber:
            raise HTTPException(status_code=404, detail="구독자를 찾을 수 없습니다")
        return subscriber
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
