"""LLM service interfaces for different capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ILLMProvider(ABC):
    """Base interface for LLM providers."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured data from prompt."""
        pass


class ITextProcessor(ABC):
    """Interface for text processing capabilities."""
    
    @abstractmethod
    async def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        pass
    
    @abstractmethod
    async def extract_keywords(self, text: str, count: int = 10) -> List[str]:
        """Extract keywords from text."""
        pass
    
    @abstractmethod
    async def detect_language(self, text: str) -> str:
        """Detect text language."""
        pass


class IContentAnalyzer(ABC):
    """Interface for content analysis capabilities."""
    
    @abstractmethod
    async def is_relevant(self, text: str, criteria: Optional[Dict[str, Any]] = None) -> bool:
        """Check if content is relevant to criteria."""
        pass
    
    @abstractmethod
    async def classify_category(self, text: str, categories: Optional[List[str]] = None) -> str:
        """Classify content into categories."""
        pass
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of content."""
        pass
    
    @abstractmethod
    async def deduplicate(self, items: List[str], threshold: float = 0.8) -> List[int]:
        """Remove duplicate items and return indices to keep."""
        pass


class IContentGenerator(ABC):
    """Interface for content generation capabilities."""
    
    @abstractmethod
    async def summarize(self, text: str, sentences: int = 3, style: str = "neutral") -> str:
        """Generate summary of content."""
        pass
    
    @abstractmethod
    async def generate_title(self, content: str, style: str = "news") -> str:
        """Generate title for content."""
        pass
    
    @abstractmethod
    async def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """Generate outline for topic."""
        pass
    
    @abstractmethod
    async def rewrite(self, text: str, style: str = "professional") -> str:
        """Rewrite content in different style."""
        pass

