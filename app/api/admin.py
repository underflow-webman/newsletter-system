from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.application.dtos import CrawlRequest, HierarchicalCrawlRequest
from app.application.use_cases import CrawlAndDraftNewsletterUseCase
from app.application.use_cases.batch_crawl import BatchCrawlUseCase
from app.infrastructure.di import container


router = APIRouter()


@router.post("/crawl_manual")
async def crawl_manual(req: CrawlRequest):
    """
    수동 크롤링 + LLM 처리 + 초안 생성 트리거 엔드포인트.
    """
    try:
        use_case = CrawlAndDraftNewsletterUseCase(
            crawlers={k: v for k, v in container.crawlers_registry.get("news", {}).items()},
            llm=container.llm,
            repository=container.repository,
        )
        draft = await use_case.execute(req)
        return draft
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send_newsletter_manual")
async def send_newsletter_manual(subject: str):
    """
    IEmailSender 포트 테스트용 간단 발송 엔드포인트.
    실제 흐름에서는 DB 구독자/캠페인과 연동하여 HTML을 렌더링합니다.
    """
    try:
        result = await container.email_sender.send(
            subject=subject,
            html_body="<h1>테스트 뉴스레터</h1><p>샘플 본문</p>",
            recipients=[{"email": "test@example.com", "name": "Test User"}],
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch_crawl")
async def batch_crawl(req: HierarchicalCrawlRequest):
    """
    계층적(그룹/소스/타겟) 크롤링을 일괄 수행하고 저장.
    """
    try:
        use_case = BatchCrawlUseCase(
            crawlers=container.crawlers_registry,
            repository=container.repository,
        )
        result = await use_case.execute(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


