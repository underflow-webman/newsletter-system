from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NewsletterStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class NewsletterTemplate(Document):
    name: str
    subject_template: str
    content_template: str
    html_template: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    is_active: bool = True

    class Settings:
        name = "newsletter_templates"


class Newsletter(Document):
    title: str
    subject: str
    content: str
    html_content: Optional[str] = None
    status: NewsletterStatus = NewsletterStatus.DRAFT
    template_id: Optional[str] = None
    author_id: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    published_at: Optional[datetime] = None
    tags: List[str] = []
    metadata: dict = {}

    class Settings:
        name = "newsletters"


class NewsletterCreate(BaseModel):
    title: str
    subject: str
    content: str
    html_content: Optional[str] = None
    template_id: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}


class NewsletterUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    html_content: Optional[str] = None
    status: Optional[NewsletterStatus] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None
