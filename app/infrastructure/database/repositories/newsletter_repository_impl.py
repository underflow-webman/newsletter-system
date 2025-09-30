"""뉴스레터 레포지토리 구현체 - Beanie ODM을 사용한 실제 데이터 접근."""

from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

from app.modules.newsletter.entities import Newsletter, NewsletterItem, Subscriber, NewsletterStatus
from app.modules.newsletter.repositories import NewsletterRepository, SubscriberRepository
from app.infrastructure.database.models import (
    NewsletterDocument,
    NewsletterItemDocument,
    SubscriberDocument,
)


class NewsletterRepositoryImpl(NewsletterRepository):
    """뉴스레터 레포지토리 구현체 - Beanie ODM 기반."""

    async def save(self, newsletter: Newsletter) -> str:
        """뉴스레터를 MongoDB에 저장합니다."""
        # 엔티티를 문서 모델로 변환
        newsletter_doc = NewsletterDocument(
            title=newsletter.title,
            status=newsletter.status.value,
            scheduled_at=newsletter.scheduled_at,
            sent_at=newsletter.sent_at,
            created_at=newsletter.created_at,
            updated_at=newsletter.updated_at,
        )
        
        # 아이템들 변환
        for item in newsletter.items:
            item_doc = NewsletterItemDocument(
                title=item.title,
                content=item.content,
                source=item.source,
                url=item.url,
                category=item.category,
                relevance_score=item.relevance_score,
                created_at=item.created_at,
            )
            newsletter_doc.items.append(item_doc)
        
        # 저장
        await newsletter_doc.save()
        return str(newsletter_doc.id)

    async def get_by_id(self, newsletter_id: str) -> Optional[Newsletter]:
        """ID로 뉴스레터를 조회합니다."""
        try:
            doc = await NewsletterDocument.get(PydanticObjectId(newsletter_id))
            if not doc:
                return None
            
            # 문서를 엔티티로 변환
            return self._document_to_entity(doc)
        except Exception:
            return None

    async def list_by_status(self, status: str) -> List[Newsletter]:
        """상태별 뉴스레터 목록을 조회합니다."""
        docs = await NewsletterDocument.find(
            NewsletterDocument.status == status
        ).to_list()
        
        return [self._document_to_entity(doc) for doc in docs]

    async def update_status(self, newsletter_id: str, status: str) -> bool:
        """뉴스레터 상태를 업데이트합니다."""
        try:
            doc = await NewsletterDocument.get(PydanticObjectId(newsletter_id))
            if not doc:
                return False
            
            doc.status = status
            await doc.save()
            return True
        except Exception:
            return False

    def _document_to_entity(self, doc: NewsletterDocument) -> Newsletter:
        """문서를 엔티티로 변환합니다."""
        # 아이템들 변환
        items = []
        for item_doc in doc.items:
            item = NewsletterItem(
                id=str(item_doc.id),
                title=item_doc.title,
                content=item_doc.content,
                source=item_doc.source,
                url=item_doc.url,
                category=item_doc.category,
                relevance_score=item_doc.relevance_score,
                created_at=item_doc.created_at,
            )
            items.append(item)
        
        return Newsletter(
            id=str(doc.id),
            title=doc.title,
            items=items,
            status=NewsletterStatus(doc.status),
            scheduled_at=doc.scheduled_at,
            sent_at=doc.sent_at,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )


class SubscriberRepositoryImpl(SubscriberRepository):
    """구독자 레포지토리 구현체 - Beanie ODM 기반."""

    async def save(self, subscriber: Subscriber) -> str:
        """구독자를 MongoDB에 저장합니다."""
        doc = SubscriberDocument(
            email=subscriber.email,
            name=subscriber.name,
            categories=subscriber.categories,
            is_active=subscriber.is_active,
            subscribed_at=subscriber.subscribed_at,
            unsubscribed_at=subscriber.unsubscribed_at,
        )
        
        await doc.save()
        return str(doc.id)

    async def get_by_email(self, email: str) -> Optional[Subscriber]:
        """이메일로 구독자를 조회합니다."""
        doc = await SubscriberDocument.find_one(
            SubscriberDocument.email == email
        )
        
        if not doc:
            return None
        
        return self._document_to_entity(doc)

    async def list_active(self) -> List[Subscriber]:
        """활성 구독자 목록을 조회합니다."""
        docs = await SubscriberDocument.find(
            SubscriberDocument.is_active == True
        ).to_list()
        
        return [self._document_to_entity(doc) for doc in docs]

    async def unsubscribe(self, email: str) -> bool:
        """구독을 해지합니다."""
        try:
            doc = await SubscriberDocument.find_one(
                SubscriberDocument.email == email
            )
            if not doc:
                return False
            
            doc.is_active = False
            doc.unsubscribed_at = datetime.utcnow()
            await doc.save()
            return True
        except Exception:
            return False

    def _document_to_entity(self, doc: SubscriberDocument) -> Subscriber:
        """문서를 엔티티로 변환합니다."""
        return Subscriber(
            id=str(doc.id),
            email=doc.email,
            name=doc.name,
            categories=doc.categories,
            is_active=doc.is_active,
            subscribed_at=doc.subscribed_at,
            unsubscribed_at=doc.unsubscribed_at,
        )
