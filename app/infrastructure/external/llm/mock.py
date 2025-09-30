"""Mock LLM service for development and testing."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from .base import BaseLLMService


class MockLLM(BaseLLMService):
    """Mock LLM implementation for development and testing."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("mock", config)
    
    # ILLMProvider implementation
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate mock text."""
        return f"Mock response for: {prompt[:50]}..."
    
    async def generate_structured(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate mock structured data."""
        return {"mock": "data", "prompt": prompt[:20]}
    
    # ITextProcessor implementation
    async def clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace."""
        return " ".join(text.split())
    
    async def extract_keywords(self, text: str, count: int = 10) -> List[str]:
        """Extract mock keywords."""
        words = text.split()[:count]
        return [word.strip(".,!?") for word in words if len(word) > 3]
    
    async def detect_language(self, text: str) -> str:
        """Detect language (mock implementation)."""
        return "ko" if any(ord(char) > 127 for char in text) else "en"
    
    # IContentAnalyzer implementation
    async def is_relevant(self, text: str, criteria: Optional[Dict[str, Any]] = None) -> bool:
        """Check relevance using keyword matching."""
        criteria = criteria or self._get_default_criteria()
        keywords = criteria.get("keywords", [])
        return any(keyword in text for keyword in keywords)
    
    async def classify_category(self, text: str, categories: Optional[List[str]] = None) -> str:
        """Classify using keyword mapping."""
        categories = categories or self._get_default_categories()
        
        mapping = {
            "SKT": ["SKT", "에스케이"],
            "KT": ["KT"],
            "LGU": ["LGU", "LG U+", "엘지유플러스"],
            "방통위": ["방송통신위원회", "방통위"],
            "KAIT": ["KAIT", "한국정보통신진흥협회"],
        }
        
        for category, keywords in mapping.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        if "여론" in text:
            return "이통시장여론"
        
        return "OTHER"
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment (mock implementation)."""
        positive_words = ["좋", "긍정", "성공", "향상"]
        negative_words = ["나쁘", "부정", "실패", "악화"]
        
        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)
        
        if pos_count > neg_count:
            return {"sentiment": "positive", "score": 0.7}
        elif neg_count > pos_count:
            return {"sentiment": "negative", "score": -0.7}
        else:
            return {"sentiment": "neutral", "score": 0.0}
    
    async def deduplicate(self, items: List[str], threshold: float = 0.8) -> List[int]:
        """Remove duplicates using simple string matching."""
        seen = {}
        keep = []
        
        for idx, item in enumerate(items):
            key = item.strip().lower()
            if key not in seen:
                seen[key] = idx
                keep.append(idx)
        
        return keep
    
    # IContentGenerator implementation
    async def summarize(self, text: str, sentences: int = 3, style: str = "neutral") -> str:
        """Generate summary by truncating text."""
        words = text.split()
        if len(words) <= 20:
            return text
        
        # Simple truncation for mock
        truncated = " ".join(words[:20])
        return f"{truncated}..."
    
    async def generate_title(self, content: str, style: str = "news") -> str:
        """Generate title from content."""
        words = content.split()[:8]
        return " ".join(words) + "..."
    
    async def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """Generate outline for topic."""
        return [f"{topic} 관련 내용 {i+1}" for i in range(sections)]
    
    async def rewrite(self, text: str, style: str = "professional") -> str:
        """Rewrite text in different style."""
        return f"[{style}] {text}"

