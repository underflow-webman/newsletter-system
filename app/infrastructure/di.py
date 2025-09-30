"""의존성 주입 컨테이너 - 새로운 모듈 구조에 맞는 DI 관리."""

from __future__ import annotations

from typing import Dict, Optional, Any
from app.infrastructure.config.database import db
from app.infrastructure.database.repositories import (
    NewsletterRepositoryImpl,
    SubscriberRepositoryImpl,
    CrawledPostRepositoryImpl,
    CrawlSessionRepositoryImpl,
    EvaluationResultRepositoryImpl,
    EvaluationSessionRepositoryImpl,
)
from app.modules.newsletter.repositories import NewsletterRepository, SubscriberRepository
from app.modules.crawling.repositories import CrawledPostRepository, CrawlSessionRepository
from app.modules.evaluation.repositories import EvaluationResultRepository, EvaluationSessionRepository


class Container:
    """의존성 주입 컨테이너 - 새로운 모듈 구조에 맞는 DI 관리."""

    def __init__(self) -> None:
        self._repositories: Dict[str, Any] = {}
        self._initialized = False

    async def initialize(self) -> None:
        """컨테이너를 초기화합니다."""
        if self._initialized:
            return

        # 데이터베이스 연결 초기화
        from app.infrastructure.config.database import init_db
        await init_db()

        # 레포지토리 구현체들 생성
        self._repositories = {
            # 뉴스레터 레포지토리들
            "newsletter_repository": NewsletterRepositoryImpl(),
            "subscriber_repository": SubscriberRepositoryImpl(),
            
            # 크롤링 레포지토리들
            "crawled_post_repository": CrawledPostRepositoryImpl(),
            "crawl_session_repository": CrawlSessionRepositoryImpl(),
            
            # 평가 레포지토리들
            "evaluation_result_repository": EvaluationResultRepositoryImpl(),
            "evaluation_session_repository": EvaluationSessionRepositoryImpl(),
        }

        self._initialized = True

    def get_newsletter_repository(self) -> NewsletterRepository:
        """뉴스레터 레포지토리를 가져옵니다."""
        return self._repositories["newsletter_repository"]

    def get_subscriber_repository(self) -> SubscriberRepository:
        """구독자 레포지토리를 가져옵니다."""
        return self._repositories["subscriber_repository"]

    def get_crawled_post_repository(self) -> CrawledPostRepository:
        """크롤링된 게시글 레포지토리를 가져옵니다."""
        return self._repositories["crawled_post_repository"]

    def get_crawl_session_repository(self) -> CrawlSessionRepository:
        """크롤링 세션 레포지토리를 가져옵니다."""
        return self._repositories["crawl_session_repository"]

    def get_evaluation_result_repository(self) -> EvaluationResultRepository:
        """평가 결과 레포지토리를 가져옵니다."""
        return self._repositories["evaluation_result_repository"]

    def get_evaluation_session_repository(self) -> EvaluationSessionRepository:
        """평가 세션 레포지토리를 가져옵니다."""
        return self._repositories["evaluation_session_repository"]

    async def cleanup(self) -> None:
        """컨테이너를 정리합니다."""
        if not self._initialized:
            return

        # 데이터베이스 연결 종료
        from app.infrastructure.config.database import close_db
        await close_db()

        self._initialized = False


# 전역 컨테이너 인스턴스
container = Container()