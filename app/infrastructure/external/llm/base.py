"""Base LLM service implementation."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from app.domain.ports import ILLMService
from .interfaces import ILLMProvider, ITextProcessor, IContentAnalyzer, IContentGenerator


class BaseLLMService(ILLMService, ILLMProvider, ITextProcessor, IContentAnalyzer, IContentGenerator):
    """Base implementation for LLM services with common functionality."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the LLM service."""
        if not self._initialized:
            await self._setup_provider()
            self._initialized = True
    
    async def _setup_provider(self) -> None:
        """Setup the underlying LLM provider."""
        # Override in subclasses
        pass
    
    # ILLMService implementation
    async def is_relevant(self, text: str) -> bool:
        """Check if content is relevant."""
        return await self.is_relevant(text, self._get_default_criteria())
    
    async def deduplicate(self, items: List[str]) -> List[int]:
        """Remove duplicates from items."""
        return await self.deduplicate(items, threshold=0.8)
    
    async def classify_category(self, text: str) -> str:
        """Classify content into category."""
        return await self.classify_category(text, self._get_default_categories())
    
    async def summarize(self, text: str, sentences: int = 3) -> str:
        """Summarize content."""
        return await self.summarize(text, sentences, "neutral")
    
    # Helper methods
    def _get_default_criteria(self) -> Dict[str, Any]:
        """Get default relevance criteria."""
        return {
            "keywords": ["통신", "5G", "이통", "KT", "SKT", "LGU", "방통위", "KAIT"],
            "min_length": 10
        }
    
    def _get_default_categories(self) -> List[str]:
        """Get default categories for classification."""
        return ["SKT", "KT", "LGU", "방통위", "KAIT", "이통시장여론", "OTHER"]

