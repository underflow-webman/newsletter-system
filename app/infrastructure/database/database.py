"""데이터베이스 연결 및 초기화 - MongoDB Beanie ODM 설정."""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
import logging

from app.settings import settings
from app.infrastructure.database.models.crawling_models import CrawledPostDocument, CrawlSessionDocument
from app.infrastructure.database.models.evaluation_models import EvaluationResultDocument, EvaluationSessionDocument
from app.infrastructure.database.models.newsletter_models import NewsletterDocument, NewsletterItemDocument, SubscriberDocument


logger = logging.getLogger(__name__)

# 전역 MongoDB 클라이언트
client: Optional[AsyncIOMotorClient] = None


async def init_database() -> None:
    """데이터베이스 연결을 초기화하고 Beanie ODM을 설정합니다."""
    global client
    
    try:
        # MongoDB 클라이언트 생성
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MAX_POOL_SIZE,
            minPoolSize=settings.MIN_POOL_SIZE,
            maxIdleTimeMS=settings.MAX_IDLE_TIME_MS,
            serverSelectionTimeoutMS=settings.QUERY_TIMEOUT_MS
        )
        
        # 데이터베이스 연결 테스트
        await client.admin.command('ping')
        logger.info(f"✅ MongoDB 연결 성공: {settings.MONGODB_URL}")
        
        # Beanie ODM 초기화
        await init_beanie(
            database=client[settings.DATABASE_NAME],
            document_models=[
                # 크롤링 관련 모델
                CrawledPostDocument,
                CrawlSessionDocument,
                # 평가 관련 모델
                EvaluationResultDocument,
                EvaluationSessionDocument,
                # 뉴스레터 관련 모델
                NewsletterDocument,
                NewsletterItemDocument,
                SubscriberDocument,
            ]
        )
        
        logger.info(f"✅ Beanie ODM 초기화 완료: {settings.DATABASE_NAME}")
        
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")
        raise


async def close_database() -> None:
    """데이터베이스 연결을 종료합니다."""
    global client
    
    if client:
        client.close()
        logger.info("✅ MongoDB 연결 종료")


def get_database_client() -> AsyncIOMotorClient:
    """MongoDB 클라이언트를 반환합니다."""
    if not client:
        raise RuntimeError("데이터베이스가 초기화되지 않았습니다. init_database()를 먼저 호출하세요.")
    return client
