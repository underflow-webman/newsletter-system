from typing import List, Optional
from beanie import PydanticObjectId
from datetime import datetime

from app.models.campaign import Campaign, CampaignCreate, CampaignUpdate, CampaignStats, CampaignStatus
from app.models.newsletter import Newsletter
from app.models.subscriber import Subscriber
from app.services.daou_office_service import daou_office_service


class CampaignService:
    async def create_campaign(self, campaign_data: CampaignCreate) -> Campaign:
        """캠페인 생성"""
        # 뉴스레터 존재 확인
        newsletter = await Newsletter.get(campaign_data.newsletter_id)
        if not newsletter:
            raise ValueError("뉴스레터를 찾을 수 없습니다")
        
        # 구독자 수 계산
        total_recipients = len(campaign_data.subscriber_list)
        
        campaign = Campaign(
            **campaign_data.dict(),
            created_by="system",  # TODO: 실제 사용자 ID로 변경
            total_recipients=total_recipients,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        await campaign.save()
        return campaign

    async def get_campaigns(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[CampaignStatus] = None,
        search: Optional[str] = None
    ) -> List[Campaign]:
        """캠페인 목록 조회"""
        query = {}
        
        if status:
            query["status"] = status
            
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}}
            ]
        
        campaigns = await Campaign.find(query).skip(skip).limit(limit).sort("-created_at").to_list()
        return campaigns

    async def get_campaign(self, campaign_id: PydanticObjectId) -> Optional[Campaign]:
        """특정 캠페인 조회"""
        return await Campaign.get(campaign_id)

    async def update_campaign(
        self,
        campaign_id: PydanticObjectId,
        campaign_data: CampaignUpdate
    ) -> Optional[Campaign]:
        """캠페인 수정"""
        campaign = await Campaign.get(campaign_id)
        if not campaign:
            return None
            
        update_data = campaign_data.dict(exclude_unset=True)
        
        # 구독자 리스트가 변경된 경우 총 수신자 수 업데이트
        if "subscriber_list" in update_data:
            update_data["total_recipients"] = len(update_data["subscriber_list"])
        
        update_data["updated_at"] = datetime.utcnow()
        
        await campaign.update({"$set": update_data})
        return await Campaign.get(campaign_id)

    async def delete_campaign(self, campaign_id: PydanticObjectId) -> bool:
        """캠페인 삭제"""
        campaign = await Campaign.get(campaign_id)
        if not campaign:
            return False
            
        await campaign.delete()
        return True

    async def send_campaign(self, campaign_id: PydanticObjectId) -> dict:
        """캠페인 발송"""
        campaign = await Campaign.get(campaign_id)
        if not campaign:
            raise ValueError("캠페인을 찾을 수 없습니다")
        
        if campaign.status != CampaignStatus.DRAFT:
            raise ValueError("발송 가능한 상태가 아닙니다")
        
        # 뉴스레터 정보 가져오기
        newsletter = await Newsletter.get(campaign.newsletter_id)
        if not newsletter:
            raise ValueError("뉴스레터를 찾을 수 없습니다")
        
        # 구독자 정보 가져오기
        subscribers = await Subscriber.find(
            {"_id": {"$in": campaign.subscriber_list}, "status": "active"}
        ).to_list()
        
        if not subscribers:
            raise ValueError("발송할 구독자가 없습니다")
        
        # 캠페인 상태를 발송 중으로 변경
        await campaign.update({
            "$set": {
                "status": CampaignStatus.SENDING,
                "updated_at": datetime.utcnow()
            }
        })
        
        try:
            # 다우오피스 API를 통한 이메일 발송
            recipients = [
                {
                    "email": sub.email,
                    "name": f"{sub.first_name or ''} {sub.last_name or ''}".strip() or sub.email
                }
                for sub in subscribers
            ]
            
            result = await daou_office_service.send_bulk_email(
                recipients=recipients,
                subject=newsletter.subject,
                html_content=newsletter.html_content or newsletter.content,
                text_content=newsletter.content
            )
            
            if result["success"]:
                # 발송 성공 시 상태 업데이트
                await campaign.update({
                    "$set": {
                        "status": CampaignStatus.SENT,
                        "sent_at": datetime.utcnow(),
                        "sent_count": len(subscribers),
                        "updated_at": datetime.utcnow()
                    }
                })
                
                return {
                    "success": True,
                    "message": f"{len(subscribers)}명에게 이메일이 발송되었습니다",
                    "recipients": len(subscribers),
                    "message_id": result.get("message_id")
                }
            else:
                # 발송 실패 시 상태 롤백
                await campaign.update({
                    "$set": {
                        "status": CampaignStatus.FAILED,
                        "updated_at": datetime.utcnow()
                    }
                })
                
                return {
                    "success": False,
                    "error": result.get("error", "이메일 발송에 실패했습니다")
                }
                
        except Exception as e:
            # 오류 발생 시 상태 롤백
            await campaign.update({
                "$set": {
                    "status": CampaignStatus.FAILED,
                    "updated_at": datetime.utcnow()
                }
            })
            raise e

    async def schedule_campaign(self, campaign_id: PydanticObjectId, scheduled_at: str) -> dict:
        """캠페인 예약 발송"""
        campaign = await Campaign.get(campaign_id)
        if not campaign:
            raise ValueError("캠페인을 찾을 수 없습니다")
        
        try:
            scheduled_datetime = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("잘못된 날짜 형식입니다")
        
        if scheduled_datetime <= datetime.utcnow():
            raise ValueError("예약 시간은 현재 시간보다 미래여야 합니다")
        
        await campaign.update({
            "$set": {
                "status": CampaignStatus.SCHEDULED,
                "scheduled_at": scheduled_datetime,
                "updated_at": datetime.utcnow()
            }
        })
        
        return {
            "success": True,
            "message": f"캠페인이 {scheduled_datetime}에 발송 예약되었습니다",
            "scheduled_at": scheduled_datetime
        }

    async def get_campaign_stats(self, campaign_id: PydanticObjectId) -> Optional[CampaignStats]:
        """캠페인 통계 조회"""
        campaign = await Campaign.get(campaign_id)
        if not campaign:
            return None
        
        # 통계 계산
        total_recipients = campaign.total_recipients
        sent_count = campaign.sent_count
        delivered_count = campaign.delivered_count
        opened_count = campaign.opened_count
        clicked_count = campaign.clicked_count
        bounced_count = campaign.bounced_count
        unsubscribed_count = campaign.unsubscribed_count
        
        # 비율 계산
        open_rate = (opened_count / sent_count * 100) if sent_count > 0 else 0
        click_rate = (clicked_count / sent_count * 100) if sent_count > 0 else 0
        bounce_rate = (bounced_count / sent_count * 100) if sent_count > 0 else 0
        
        return CampaignStats(
            campaign_id=str(campaign_id),
            total_recipients=total_recipients,
            sent_count=sent_count,
            delivered_count=delivered_count,
            opened_count=opened_count,
            clicked_count=clicked_count,
            bounced_count=bounced_count,
            unsubscribed_count=unsubscribed_count,
            open_rate=round(open_rate, 2),
            click_rate=round(click_rate, 2),
            bounce_rate=round(bounce_rate, 2)
        )
