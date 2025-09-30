"""API 라우터 통합 - 모든 API 엔드포인트를 하나로 관리합니다."""

from fastapi import APIRouter
from . import newsletter, admin

# 메인 API 라우터 생성
router = APIRouter()

# 하위 라우터들 등록
router.include_router(newsletter.router, prefix="/newsletter", tags=["뉴스레터"])
router.include_router(admin.router, prefix="/admin", tags=["관리자"])

__all__ = ["router", "newsletter", "admin"]
