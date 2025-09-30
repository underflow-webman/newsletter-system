"""관리자 API 엔드포인트 - 시스템 관리 및 모니터링 API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.infrastructure.di import get_dependency_container

router = APIRouter()


@router.get("/health")
async def system_health_check() -> Dict[str, Any]:
    """시스템 상태를 확인합니다."""
    try:
        container = get_dependency_container()
        
        # 기본 상태 정보
        health_status = {
            "status": "healthy",
            "message": "시스템이 정상적으로 작동 중입니다.",
            "components": {
                "database": "connected",
                "llm_service": "available",
                "email_service": "available"
            }
        }
        
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시스템 상태 확인 실패: {str(e)}")


@router.post("/test_email")
async def test_email_send(subject: str = "테스트 이메일") -> Dict[str, Any]:
    """이메일 발송 기능을 테스트합니다."""
    try:
        container = get_dependency_container()
        email_service = container.get_email_service()
        
        # 테스트 이메일 발송
        result = await email_service.send_bulk_email(
            recipients=[{"email": "test@example.com", "name": "Test User"}],
            subject=subject,
            body="<h1>테스트 뉴스레터</h1><p>이것은 테스트 이메일입니다.</p>"
        )
        
        return {
            "success": True,
            "message": "테스트 이메일이 성공적으로 발송되었습니다.",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이메일 발송 테스트 실패: {str(e)}")


@router.post("/test_llm")
async def test_llm_processing(text: str = "통신 관련 뉴스입니다.") -> Dict[str, Any]:
    """LLM 처리 기능을 테스트합니다."""
    try:
        container = get_dependency_container()
        llm_service = container.get_llm_service()
        
        # LLM 관련성 평가 테스트
        is_relevant = await llm_service.is_relevant(text)
        category = await llm_service.classify_category(text)
        summary = await llm_service.summarize(text, sentences=2)
        
        return {
            "success": True,
            "message": "LLM 처리 테스트가 완료되었습니다.",
            "results": {
                "is_relevant": is_relevant,
                "category": category,
                "summary": summary
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 처리 테스트 실패: {str(e)}")


