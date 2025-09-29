from __future__ import annotations

from typing import List, Dict
from pydantic import BaseModel, Field, HttpUrl

"""
애플리케이션 계층 DTO
- CrawlRequest: 어떤 소스를 몇 개씩 수집할지 요청 모델
- CategoryNewsDTO: 카테고리별 선정된 뉴스 묶음
- NewsletterDraftDTO: 생성된 뉴스레터 초안(간단 HTML 포함)
"""


class CrawlRequest(BaseModel):
    sources: List[str] = Field(description="실행할 크롤러 소스 이름 목록")
    limit_per_source: int = 20


class CategoryNewsDTO(BaseModel):
    category: str
    items: List[Dict]


class NewsletterDraftDTO(BaseModel):
    subject: str
    categories: List[CategoryNewsDTO]
    html_content: str


class TargetOption(BaseModel):
    """세부 타겟별 옵션(페이지 수, 날짜 범위 등)을 확장 가능하게 정의."""
    pages: int = 1
    days: int = 7
    limit: int = 20


class HierarchicalCrawlRequest(BaseModel):
    """계층적 크롤 요청: 대분류 → 세부 소스 → 타겟 키/옵션."""
    # 예: {"community": {"ppomppu": {"mobile": {...}}}, "gov": {"kcc": {"press": {...}}}}
    sources: Dict[str, Dict[str, Dict[str, TargetOption]]]


