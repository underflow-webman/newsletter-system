from __future__ import annotations

from typing import Protocol, Iterable, List, Dict, Optional, runtime_checkable, Any
from dataclasses import dataclass

"""
도메인 포트(인터페이스) 정의
- ICrawler: 사이트별 크롤러 전략 인터페이스
- ILLMService: LLM 벤더/모델 추상화 인터페이스
- INewsRepository: 뉴스 관련 데이터 저장소 추상화(Repository 패턴)
- IEmailSender: 이메일 발송 어댑터 포트

DDD에서 도메인 계층은 외부 구현에 의존하지 않기 위해 인터페이스(Port)를 정의하고,
인프라 계층이 해당 Port의 구현체(Adapters)를 제공합니다.
"""


@dataclass(frozen=True)
class CrawlTarget:
    """크롤링 대상 정의(목록 URL, 출처명, 카테고리, 제한 수 등)."""
    source_name: str
    base_url: str
    category: str
    limit: int = 20


@dataclass(frozen=True)
class RawPost:
    """크롤러가 수집하는 원시 게시글 단위."""
    source_name: str
    url: str
    title: str
    content_snippet: str
    published_at: Optional[str] = None


@runtime_checkable
class ICrawler(Protocol):
    """전략(Strategy) 패턴: 사이트별로 이 인터페이스를 구현합니다."""

    async def list_posts(self, target: CrawlTarget, options: Optional[Dict[str, Any]] = None) -> List[RawPost]:
        ...


@runtime_checkable
class ILLMService(Protocol):
    """LLM 공급자/모델 추상화. 프롬프트/응답 세부 구현을 감춥니다."""

    async def is_relevant(self, text: str) -> bool:
        ...

    async def deduplicate(self, items: List[str]) -> List[int]:
        """중복 제거 후 유지할 아이템 인덱스 목록을 반환."""
        ...

    async def classify_category(self, text: str) -> str:
        ...

    async def summarize(self, text: str, sentences: int = 3) -> str:
        ...


@runtime_checkable
class INewsRepository(Protocol):
    """Repository 패턴: 영속성 계층으로부터 도메인을 분리."""

    async def save_raw_posts(self, posts: List[RawPost]) -> int:
        ...

    async def save_newsletter_draft(self, draft: Dict) -> str:
        ...


@runtime_checkable
class IEmailSender(Protocol):
    """이메일 발송 포트: 다우오피스 등 다양한 공급자 교체 가능."""

    async def send(self, subject: str, html_body: str, recipients: List[Dict[str, str]]) -> Dict:
        ...


