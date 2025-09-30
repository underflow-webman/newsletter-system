"""기본 LLM 서비스 구현."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from .interfaces import ILLMProvider, ITextProcessor, IContentAnalyzer, IContentGenerator


class BaseLLMService(ILLMProvider, ITextProcessor, IContentAnalyzer, IContentGenerator):
    """공통 기능을 가진 LLM 서비스의 기본 구현."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """LLM 서비스를 초기화합니다."""
        if not self._initialized:
            await self._setup_provider()
            self._initialized = True
    
    async def _setup_provider(self) -> None:
        """기본 LLM 제공자를 설정합니다."""
        # 서브클래스에서 오버라이드
        pass
    
    # ILLMService 구현
    async def is_relevant(self, text: str) -> bool:
        """콘텐츠의 관련성을 확인합니다."""
        return await self.is_relevant(text, self._get_default_criteria())
    
    async def deduplicate(self, items: List[str]) -> List[int]:
        """항목에서 중복을 제거합니다."""
        return await self.deduplicate(items, threshold=0.8)
    
    async def classify_category(self, text: str) -> str:
        """콘텐츠를 카테고리로 분류합니다."""
        return await self.classify_category(text, self._get_default_categories())
    
    async def summarize(self, text: str, sentences: int = 3) -> str:
        """콘텐츠를 요약합니다."""
        return await self.summarize(text, sentences, "neutral")
    
    # 헬퍼 메서드
    def _get_default_criteria(self) -> Dict[str, Any]:
        """기본 관련성 기준을 가져옵니다."""
        return {
            "keywords": ["통신", "5G", "이통", "KT", "SKT", "LGU", "방통위", "KAIT"],
            "min_length": 10
        }
    
    def _get_default_categories(self) -> List[str]:
        """분류를 위한 기본 카테고리를 가져옵니다."""
        return ["SKT", "KT", "LGU", "방통위", "KAIT", "이통시장여론", "OTHER"]

