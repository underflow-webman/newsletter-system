"""Newsletter module - 뉴스레터 모듈 (독립적 DDD 구조)."""

from .entities import Newsletter, NewsletterItem, Subscriber
from .repositories import NewsletterRepository, SubscriberRepository
from .services import NewsletterService, TemplateService
from .use_cases import CreateNewsletterUseCase, SendNewsletterUseCase, DailyNewsletterUseCase

__all__ = [
    # Entities
    "Newsletter",
    "NewsletterItem", 
    "Subscriber",
    # Repositories
    "NewsletterRepository",
    "SubscriberRepository",
    # Services
    "NewsletterService",
    "TemplateService",
    # Use Cases
    "CreateNewsletterUseCase",
    "SendNewsletterUseCase",
    "DailyNewsletterUseCase",
]
