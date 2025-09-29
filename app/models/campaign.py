from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Campaign(Document):
    name: str
    newsletter_id: str
    subscriber_list: List[str]  # Subscriber IDs
    status: CampaignStatus = CampaignStatus.DRAFT
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    created_by: str
    metadata: dict = {}
    
    # 통계 정보
    total_recipients: int = 0
    sent_count: int = 0
    delivered_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    bounced_count: int = 0
    unsubscribed_count: int = 0

    class Settings:
        name = "campaigns"


class CampaignCreate(BaseModel):
    name: str
    newsletter_id: str
    subscriber_list: List[str]
    scheduled_at: Optional[datetime] = None
    metadata: dict = {}


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subscriber_list: Optional[List[str]] = None
    status: Optional[CampaignStatus] = None
    scheduled_at: Optional[datetime] = None
    metadata: Optional[dict] = None


class CampaignStats(BaseModel):
    campaign_id: str
    total_recipients: int
    sent_count: int
    delivered_count: int
    opened_count: int
    clicked_count: int
    bounced_count: int
    unsubscribed_count: int
    open_rate: float
    click_rate: float
    bounce_rate: float
