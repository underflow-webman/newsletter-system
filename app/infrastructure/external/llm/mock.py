"""개발 및 테스트용 Mock LLM 서비스."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from .base import BaseLLMService


class MockLLM(BaseLLMService):
    """개발 및 테스트용 Mock LLM 구현."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("mock", config)
    
    # ILLMProvider 구현
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Mock 텍스트를 생성합니다."""
        return f"Mock response for: {prompt[:50]}..."
    
    async def generate_structured(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Mock 구조화된 데이터를 생성합니다."""
        return {"mock": "data", "prompt": prompt[:20]}
    
    # ITextProcessor 구현
    async def clean_text(self, text: str) -> str:
        """여분의 공백을 제거하여 텍스트를 정리합니다."""
        return " ".join(text.split())
    
    async def extract_keywords(self, text: str, count: int = 10) -> List[str]:
        """Mock 키워드를 추출합니다."""
        words = text.split()[:count]
        return [word.strip(".,!?") for word in words if len(word) > 3]
    
    async def detect_language(self, text: str) -> str:
        """언어를 감지합니다 (Mock 구현)."""
        return "ko" if any(ord(char) > 127 for char in text) else "en"
    
    # IContentAnalyzer 구현
    async def is_relevant(self, text: str, criteria: Optional[Dict[str, Any]] = None) -> bool:
        """키워드 매칭을 사용하여 관련성을 확인합니다."""
        criteria = criteria or self._get_default_criteria()
        keywords = criteria.get("keywords", [])
        return any(keyword in text for keyword in keywords)
    
    async def classify_category(self, text: str, categories: Optional[List[str]] = None) -> str:
        """키워드 매핑을 사용하여 분류합니다."""
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
        """감정을 분석합니다 (Mock 구현)."""
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
        """간단한 문자열 매칭을 사용하여 중복을 제거합니다."""
        seen = {}
        keep = []
        
        for idx, item in enumerate(items):
            key = item.strip().lower()
            if key not in seen:
                seen[key] = idx
                keep.append(idx)
        
        return keep
    
    # IContentGenerator 구현
    async def summarize(self, text: str, sentences: int = 3, style: str = "neutral") -> str:
        """텍스트를 잘라서 요약을 생성합니다."""
        words = text.split()
        if len(words) <= 20:
            return text
        
        # Mock을 위한 간단한 잘라내기
        truncated = " ".join(words[:20])
        return f"{truncated}..."
    
    async def generate_title(self, content: str, style: str = "news") -> str:
        """콘텐츠에서 제목을 생성합니다."""
        words = content.split()[:8]
        return " ".join(words) + "..."
    
    async def generate_outline(self, topic: str, sections: int = 5) -> List[str]:
        """주제에 대한 개요를 생성합니다."""
        return [f"{topic} 관련 내용 {i+1}" for i in range(sections)]
    
    async def rewrite(self, text: str, style: str = "professional") -> str:
        """다른 스타일로 텍스트를 다시 작성합니다."""
        return f"[{style}] {text}"

