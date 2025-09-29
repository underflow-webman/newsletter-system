from typing import List, Optional
from beanie import PydanticObjectId
from datetime import datetime
import uuid

from app.models.subscriber import Subscriber, SubscriberCreate, SubscriberUpdate, SubscriberBulkImport, SubscriptionStatus


class SubscriberService:
    async def create_subscriber(self, subscriber_data: SubscriberCreate) -> Subscriber:
        """구독자 생성"""
        # 이메일 중복 확인
        existing = await self.get_subscriber_by_email(subscriber_data.email)
        if existing:
            raise ValueError("이미 등록된 이메일입니다")
        
        verification_token = str(uuid.uuid4())
        
        subscriber = Subscriber(
            **subscriber_data.dict(),
            verification_token=verification_token,
            subscribed_at=datetime.utcnow()
        )
        await subscriber.save()
        return subscriber

    async def bulk_import_subscribers(self, import_data: SubscriberBulkImport) -> dict:
        """구독자 대량 등록"""
        success_count = 0
        error_count = 0
        errors = []
        
        for subscriber_data in import_data.subscribers:
            try:
                # 공통 태그 추가
                if import_data.tags:
                    subscriber_data.tags.extend(import_data.tags)
                
                await self.create_subscriber(subscriber_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append({
                    "email": subscriber_data.email,
                    "error": str(e)
                })
        
        return {
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors
        }

    async def get_subscribers(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[SubscriptionStatus] = None,
        search: Optional[str] = None
    ) -> List[Subscriber]:
        """구독자 목록 조회"""
        query = {}
        
        if status:
            query["status"] = status
            
        if search:
            query["$or"] = [
                {"email": {"$regex": search, "$options": "i"}},
                {"first_name": {"$regex": search, "$options": "i"}},
                {"last_name": {"$regex": search, "$options": "i"}}
            ]
        
        subscribers = await Subscriber.find(query).skip(skip).limit(limit).sort("-subscribed_at").to_list()
        return subscribers

    async def get_subscriber(self, subscriber_id: PydanticObjectId) -> Optional[Subscriber]:
        """특정 구독자 조회"""
        return await Subscriber.get(subscriber_id)

    async def get_subscriber_by_email(self, email: str) -> Optional[Subscriber]:
        """이메일로 구독자 조회"""
        return await Subscriber.find_one(Subscriber.email == email)

    async def update_subscriber(
        self,
        subscriber_id: PydanticObjectId,
        subscriber_data: SubscriberUpdate
    ) -> Optional[Subscriber]:
        """구독자 정보 수정"""
        subscriber = await Subscriber.get(subscriber_id)
        if not subscriber:
            return None
            
        update_data = subscriber_data.dict(exclude_unset=True)
        
        await subscriber.update({"$set": update_data})
        return await Subscriber.get(subscriber_id)

    async def delete_subscriber(self, subscriber_id: PydanticObjectId) -> bool:
        """구독자 삭제"""
        subscriber = await Subscriber.get(subscriber_id)
        if not subscriber:
            return False
            
        await subscriber.delete()
        return True

    async def unsubscribe_subscriber(self, subscriber_id: PydanticObjectId) -> Optional[Subscriber]:
        """구독 해지"""
        subscriber = await Subscriber.get(subscriber_id)
        if not subscriber:
            return None
            
        await subscriber.update({
            "$set": {
                "status": SubscriptionStatus.UNSUBSCRIBED,
                "unsubscribed_at": datetime.utcnow()
            }
        })
        return await Subscriber.get(subscriber_id)

    async def verify_subscriber(self, verification_token: str) -> Optional[Subscriber]:
        """구독자 이메일 인증"""
        subscriber = await Subscriber.find_one(Subscriber.verification_token == verification_token)
        if not subscriber:
            return None
            
        await subscriber.update({
            "$set": {
                "is_verified": True,
                "verification_token": None
            }
        })
        return await Subscriber.get(subscriber.id)
