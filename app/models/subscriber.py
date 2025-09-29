from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    COMPLAINED = "complained"


class Subscriber(Document):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    subscribed_at: datetime = datetime.utcnow()
    unsubscribed_at: Optional[datetime] = None
    tags: List[str] = []
    metadata: dict = {}
    is_verified: bool = False
    verification_token: Optional[str] = None

    class Settings:
        name = "subscribers"
        indexes = [
            "email",
            "status",
            "subscribed_at"
        ]


class SubscriberCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}


class SubscriberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[SubscriptionStatus] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None


class SubscriberBulkImport(BaseModel):
    subscribers: List[SubscriberCreate]
    tags: List[str] = []
