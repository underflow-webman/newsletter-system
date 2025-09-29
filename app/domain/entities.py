from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

"""
도메인 엔티티/값 객체 정의
- Category: 통신사/기관/여론 카테고리 구분
- Summary: 요약 결과 보유(기본 3문장)
- NewsItem: 뉴스 항목(출처, URL, 카테고리, 요약 포함)
"""


class Category(str, Enum):
    SKT = "SKT"
    KT = "KT"
    LGU = "LGU"
    BROADCASTING_COMMISSION = "방통위"
    KAIT = "KAIT"
    MARKET_OPINION = "이통시장여론"
    OTHER = "OTHER"


@dataclass
class Summary:
    """LLM 요약 결과를 담는 값 객체."""
    text: str
    sentences: int = 3


@dataclass
class NewsItem:
    """뉴스 항목 도메인 엔티티."""
    title: str
    url: str
    source_name: str
    category: Category
    summary: Optional[Summary] = None
    score: float = 0.0
    original_excerpt: Optional[str] = None


