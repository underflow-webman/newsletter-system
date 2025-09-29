from typing import List, Optional
from beanie import PydanticObjectId
from datetime import datetime

from app.models.newsletter import Newsletter, NewsletterCreate, NewsletterUpdate, NewsletterStatus


class NewsletterService:
    async def create_newsletter(self, newsletter_data: NewsletterCreate) -> Newsletter:
        """뉴스레터 생성"""
        newsletter = Newsletter(
            **newsletter_data.dict(),
            author_id="system",  # TODO: 실제 사용자 ID로 변경
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await newsletter.save()
        return newsletter

    async def get_newsletters(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[NewsletterStatus] = None,
        search: Optional[str] = None
    ) -> List[Newsletter]:
        """뉴스레터 목록 조회"""
        query = {}
        
        if status:
            query["status"] = status
            
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"subject": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}}
            ]
        
        newsletters = await Newsletter.find(query).skip(skip).limit(limit).sort("-created_at").to_list()
        return newsletters

    async def get_newsletter(self, newsletter_id: PydanticObjectId) -> Optional[Newsletter]:
        """특정 뉴스레터 조회"""
        return await Newsletter.get(newsletter_id)

    async def update_newsletter(
        self,
        newsletter_id: PydanticObjectId,
        newsletter_data: NewsletterUpdate
    ) -> Optional[Newsletter]:
        """뉴스레터 수정"""
        newsletter = await Newsletter.get(newsletter_id)
        if not newsletter:
            return None
            
        update_data = newsletter_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        await newsletter.update({"$set": update_data})
        return await Newsletter.get(newsletter_id)

    async def delete_newsletter(self, newsletter_id: PydanticObjectId) -> bool:
        """뉴스레터 삭제"""
        newsletter = await Newsletter.get(newsletter_id)
        if not newsletter:
            return False
            
        await newsletter.delete()
        return True

    async def publish_newsletter(self, newsletter_id: PydanticObjectId) -> Optional[Newsletter]:
        """뉴스레터 발행"""
        newsletter = await Newsletter.get(newsletter_id)
        if not newsletter:
            return None
            
        await newsletter.update({
            "$set": {
                "status": NewsletterStatus.PUBLISHED,
                "published_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        })
        return await Newsletter.get(newsletter_id)
