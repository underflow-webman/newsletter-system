"""Claude LLM service implementation."""

from __future__ import annotations

from typing import List, Dict, Any, Optional
import anthropic
from .base import BaseLLMService


class ClaudeService(BaseLLMService):
    """Claude LLM service implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("claude", config)
        self.api_key = self.config.get("api_key")
        self.model = self.config.get("model", "claude-3-sonnet-20240229")
        self.client = None
    
    async def _setup_provider(self) -> None:
        """Setup Claude client."""
        if not self.api_key:
            raise ValueError("Claude API key is required")
        
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
    
    # ILLMProvider implementation
    async def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Claude API."""
        if not self.client:
            await self.initialize()
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1000),
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        return response.content[0].text
    
    async def generate_structured(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured data using Claude API."""
        # Implementation for structured generation
        response = await self.generate_text(prompt, **kwargs)
        # Parse response based on schema
        return {"generated": response}
    
    # IContentAnalyzer implementation
    async def is_relevant(self, text: str, criteria: Optional[Dict[str, Any]] = None) -> bool:
        """Check relevance using Claude."""
        criteria = criteria or self._get_default_criteria()
        keywords = criteria.get("keywords", [])
        
        prompt = f"""
        다음 텍스트가 통신/IT 관련 주제와 관련이 있는지 판단해주세요.
        관련 키워드: {', '.join(keywords)}
        
        텍스트: {text}
        
        관련성이 있으면 'YES', 없으면 'NO'로 답변해주세요.
        """
        
        response = await self.generate_text(prompt)
        return "YES" in response.upper()
    
    async def classify_category(self, text: str, categories: Optional[List[str]] = None) -> str:
        """Classify content using Claude."""
        categories = categories or self._get_default_categories()
        
        prompt = f"""
        다음 텍스트를 다음 카테고리 중 하나로 분류해주세요:
        {', '.join(categories)}
        
        텍스트: {text}
        
        가장 적절한 카테고리명만 답변해주세요.
        """
        
        response = await self.generate_text(prompt)
        return response.strip()
    
    async def summarize(self, text: str, sentences: int = 3, style: str = "neutral") -> str:
        """Generate summary using Claude."""
        prompt = f"""
        다음 텍스트를 {sentences}문장으로 요약해주세요.
        스타일: {style}
        
        텍스트: {text}
        """
        
        return await self.generate_text(prompt)

