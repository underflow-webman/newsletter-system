"""뉴스레터 시스템 메인 애플리케이션 - FastAPI 기반 웹 서버."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
import asyncio
import logging

from app.settings import settings
from app.infrastructure.database.database import init_database
from app.api.routes import router as api_router
from app.modules.newsletter.use_cases import DailyNewsletterUseCase
from app.infrastructure.di import get_dependency_container


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리 - 시작/종료 시 실행할 작업들."""
    # 시작 시 실행
    logger.info("🚀 뉴스레터 시스템 시작 중...")
    
    try:
        # 데이터베이스 초기화 (선택적)
        try:
            await init_database()
            logger.info("✅ 데이터베이스 연결 완료")
        except Exception as db_error:
            logger.warning(f"⚠️ 데이터베이스 연결 실패 (계속 진행): {db_error}")
        
        # 의존성 컨테이너 초기화
        container = get_dependency_container()
        await container.init_resources()
        logger.info("✅ 의존성 주입 컨테이너 초기화 완료")
        
        logger.info("✅ 뉴스레터 시스템 시작 완료")
        
    except Exception as e:
        logger.error(f"❌ 시스템 시작 실패: {e}")
        # 데이터베이스 없이도 계속 진행
        logger.info("⚠️ 데이터베이스 없이 계속 진행합니다.")
    
    yield
    
    # 종료 시 실행
    logger.info("🛑 뉴스레터 시스템 종료 중...")
    
    try:
        # 의존성 컨테이너 정리
        container = get_dependency_container()
        await container.shutdown_resources()
        logger.info("✅ 의존성 주입 컨테이너 정리 완료")
        
        logger.info("✅ 뉴스레터 시스템 종료 완료")
        
    except Exception as e:
        logger.error(f"❌ 시스템 종료 중 오류: {e}")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="통신/IT 관련 뉴스레터 자동 생성 및 발송 시스템",
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> Dict[str, str]:
    """루트 엔드포인트 - 시스템 상태 확인."""
    return {
        "message": "뉴스레터 시스템이 정상적으로 실행 중입니다.",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """헬스체크 엔드포인트 - 시스템 상태 확인."""
    return {
        "status": "healthy",
        "message": "시스템이 정상적으로 작동 중입니다."
    }


@app.post("/newsletter/daily")
async def create_daily_newsletter() -> Dict[str, Any]:
    """일일 뉴스레터 생성 및 발송 엔드포인트."""
    try:
        # 의존성 컨테이너에서 필요한 서비스들 가져오기
        container = get_dependency_container()
        
        # DailyNewsletterUseCase 인스턴스 생성
        daily_newsletter_use_case = container.get_daily_newsletter_use_case()
        
        # 일일 뉴스레터 실행
        result = await daily_newsletter_use_case.execute()
        
        return {
            "success": True,
            "message": "일일 뉴스레터가 성공적으로 생성되고 발송되었습니다.",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"일일 뉴스레터 생성 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"일일 뉴스레터 생성 중 오류가 발생했습니다: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
