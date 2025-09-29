from __future__ import annotations

from typing import List

from app.domain.ports import ILLMService


class MockLLM(ILLMService):
    """모킹 LLM 구현: 로컬 개발 시 빠르고 결정적으로 동작."""

    async def is_relevant(self, text: str) -> bool:
        keywords = ["통신", "5G", "이통", "KT", "SKT", "LGU", "방통위", "KAIT"]
        return any(k in text for k in keywords)

    async def deduplicate(self, items: List[str]) -> List[int]:
        """대소문자/공백 정규화 기준으로 처음 등장한 항목만 유지."""
        seen = {}
        keep = []
        for idx, t in enumerate(items):
            key = t.strip().lower()
            if key not in seen:
                seen[key] = idx
                keep.append(idx)
        return keep

    async def classify_category(self, text: str) -> str:
        mapping = {
            "SKT": ["SKT", "에스케이"],
            "KT": ["KT"],
            "LGU": ["LGU", "LG U+", "엘지유플러스"],
            "방통위": ["방송통신위원회", "방통위"],
            "KAIT": ["KAIT", "한국정보통신진흥협회"],
        }
        for cat, keys in mapping.items():
            if any(k in text for k in keys):
                return cat
        if "여론" in text:
            return "이통시장여론"
        return "OTHER"

    async def summarize(self, text: str, sentences: int = 3) -> str:
        """간단 절단 기반 요약(데모용). 실제로는 벤더 API 호출."""
        return (text[:200] + "...") if len(text) > 200 else text


