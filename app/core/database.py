from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.newsletter import Newsletter
from app.models.subscriber import Subscriber
from app.models.campaign import Campaign
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    return db.database

async def init_db():
    """데이터베이스 연결 초기화"""
    try:
        # MongoDB 클라이언트 생성
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Beanie 초기화
        await init_beanie(
            database=db.database,
            document_models=[Newsletter, Subscriber, Campaign]
        )
        
        logger.info("데이터베이스 연결이 성공적으로 초기화되었습니다.")
        
    except Exception as e:
        logger.error(f"데이터베이스 연결 초기화 실패: {e}")
        raise

async def close_db():
    """데이터베이스 연결 종료"""
    if db.client:
        db.client.close()
        logger.info("데이터베이스 연결이 종료되었습니다.")
