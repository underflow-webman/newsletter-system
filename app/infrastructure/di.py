"""의존성 주입 컨테이너 - 새로운 모듈 구조에 맞는 DI 관리."""

from __future__ import annotations

import logging
from typing import Dict, Optional, Any
from app.infrastructure.database.database import get_database_client
from app.infrastructure.database.repositories import (
    NewsletterRepositoryImpl,
    CrawledPostRepositoryImpl,
    CrawlSessionRepositoryImpl,
    EvaluationResultRepositoryImpl,
    EvaluationSessionRepositoryImpl,
)
from app.modules.newsletter.repositories import NewsletterRepository, SubscriberRepository
from app.modules.crawling.repositories import CrawledPostRepository, CrawlSessionRepository
from app.modules.evaluation.repositories import EvaluationResultRepository, EvaluationSessionRepository
from app.modules.newsletter.services import NewsletterService, TemplateService
from app.modules.newsletter.use_cases import DailyNewsletterUseCase
from app.infrastructure.external.llm.mock import MockLLM
from app.infrastructure.external.email.smtp import SMTPEmailService

logger = logging.getLogger(__name__)


class Container:
    """의존성 주입 컨테이너 - 새로운 모듈 구조에 맞는 DI 관리."""

    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}
        self._initialized = False

    async def init_resources(self) -> None:
        """컨테이너 리소스를 초기화합니다."""
        if self._initialized:
            return

        # 데이터베이스 클라이언트 가져오기 (선택적)
        try:
            db_client = get_database_client()
        except Exception as e:
            logger.warning(f"데이터베이스 클라이언트를 가져올 수 없습니다: {e}")
            db_client = None

        # 레포지토리 구현체들 생성
        newsletter_repo = NewsletterRepositoryImpl()
        crawled_post_repo = CrawledPostRepositoryImpl()
        crawl_session_repo = CrawlSessionRepositoryImpl()
        evaluation_result_repo = EvaluationResultRepositoryImpl()
        evaluation_session_repo = EvaluationSessionRepositoryImpl()

        # 서비스들 생성 (SubscriberRepository는 None으로 설정)
        newsletter_service = NewsletterService(newsletter_repo, None)
        template_service = TemplateService()
        
        # 외부 서비스들 생성 (개발용 Mock 사용)
        llm_service = MockLLM()
        email_service = SMTPEmailService()

        # 서비스들을 컨테이너에 저장
        self._services = {
            # 레포지토리들
            "newsletter_repository": newsletter_repo,
            "crawled_post_repository": crawled_post_repo,
            "crawl_session_repository": crawl_session_repo,
            "evaluation_result_repository": evaluation_result_repo,
            "evaluation_session_repository": evaluation_session_repo,
            
            # 서비스들
            "newsletter_service": newsletter_service,
            "template_service": template_service,
            "llm_service": llm_service,
            "email_service": email_service,
        }

        self._initialized = True

    def get_newsletter_repository(self) -> NewsletterRepository:
        """뉴스레터 레포지토리를 가져옵니다."""
        return self._services["newsletter_repository"]

    def get_subscriber_repository(self) -> SubscriberRepository:
        """구독자 레포지토리를 가져옵니다."""
        return None  # SubscriberRepository는 아직 구현되지 않음

    def get_crawled_post_repository(self) -> CrawledPostRepository:
        """크롤링된 게시글 레포지토리를 가져옵니다."""
        return self._services["crawled_post_repository"]

    def get_crawl_session_repository(self) -> CrawlSessionRepository:
        """크롤링 세션 레포지토리를 가져옵니다."""
        return self._services["crawl_session_repository"]

    def get_evaluation_result_repository(self) -> EvaluationResultRepository:
        """평가 결과 레포지토리를 가져옵니다."""
        return self._services["evaluation_result_repository"]

    def get_evaluation_session_repository(self) -> EvaluationSessionRepository:
        """평가 세션 레포지토리를 가져옵니다."""
        return self._services["evaluation_session_repository"]

    def get_newsletter_service(self) -> NewsletterService:
        """뉴스레터 서비스를 가져옵니다."""
        return self._services["newsletter_service"]

    def get_template_service(self) -> TemplateService:
        """템플릿 서비스를 가져옵니다."""
        return self._services["template_service"]

    def get_llm_service(self):
        """LLM 서비스를 가져옵니다."""
        return self._services["llm_service"]

    def get_email_service(self):
        """이메일 서비스를 가져옵니다."""
        return self._services["email_service"]

    def get_daily_newsletter_use_case(self) -> DailyNewsletterUseCase:
        """일일 뉴스레터 유즈케이스를 가져옵니다."""
        # TODO: 실제 크롤링 유즈케이스들 구현 후 연결
        from app.modules.crawling.use_cases import CrawlCommunityUseCase, CrawlNewsUseCase, CrawlGovernmentUseCase
        from app.modules.evaluation.use_cases import EvaluatePostsUseCase
        
        # Mock 유즈케이스들 생성 (실제 구현 전까지)
        crawl_community_use_case = None  # CrawlCommunityUseCase()
        crawl_news_use_case = None  # CrawlNewsUseCase()
        crawl_government_use_case = None  # CrawlGovernmentUseCase()
        evaluate_posts_use_case = None  # EvaluatePostsUseCase()
        
        return DailyNewsletterUseCase(
            newsletter_service=self.get_newsletter_service(),
            template_service=self.get_template_service(),
            crawl_community_use_case=crawl_community_use_case,
            crawl_news_use_case=crawl_news_use_case,
            crawl_government_use_case=crawl_government_use_case,
            evaluate_posts_use_case=evaluate_posts_use_case,
            email_sender=self.get_email_service()
        )

    async def shutdown_resources(self) -> None:
        """컨테이너 리소스를 정리합니다."""
        if not self._initialized:
            return

        # 데이터베이스 연결 종료
        from app.infrastructure.database.database import close_database
        await close_database()

        self._initialized = False


# 전역 컨테이너 인스턴스
container = Container()


def get_dependency_container() -> Container:
    """의존성 주입 컨테이너를 반환합니다."""
    return container