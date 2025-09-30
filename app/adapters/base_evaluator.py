"""기본 평가자 인터페이스 - 모든 평가자가 구현해야 하는 공통 인터페이스."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.modules.evaluation.entities import EvaluationResult


class BaseEvaluator(ABC):
    """기본 평가자 인터페이스 - 모든 평가자가 구현해야 하는 공통 인터페이스."""
    
    def __init__(self, name: str):
        """평가자를 초기화합니다.
        
        Args:
            name: 평가자 이름
        """
        self.name = name
    
    @abstractmethod
    async def evaluate(self, data: Any, **kwargs) -> EvaluationResult:
        """데이터를 평가합니다.
        
        Args:
            data: 평가할 데이터
            **kwargs: 평가 옵션
            
        Returns:
            평가 결과
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """평가자 상태를 확인합니다.
        
        Returns:
            평가자가 정상 작동하면 True, 그렇지 않으면 False
        """
        pass


class LLMEvaluator(BaseEvaluator):
    """LLM 기반 평가자 기본 클래스."""
    
    @abstractmethod
    async def evaluate_relevance(self, content: str, criteria: str) -> float:
        """관련성을 평가합니다.
        
        Args:
            content: 평가할 콘텐츠
            criteria: 평가 기준
            
        Returns:
            관련성 점수 (0.0 ~ 1.0)
        """
        pass
    
    @abstractmethod
    async def categorize(self, content: str, categories: List[str]) -> str:
        """콘텐츠를 카테고리화합니다.
        
        Args:
            content: 카테고리화할 콘텐츠
            categories: 가능한 카테고리 목록
            
        Returns:
            가장 적합한 카테고리
        """
        pass
    
    @abstractmethod
    async def summarize(self, content: str, max_length: int = 200) -> str:
        """콘텐츠를 요약합니다.
        
        Args:
            content: 요약할 콘텐츠
            max_length: 최대 요약 길이
            
        Returns:
            요약된 텍스트
        """
        pass


class RelevanceEvaluator(BaseEvaluator):
    """관련성 평가자 기본 클래스."""
    
    @abstractmethod
    async def evaluate_keywords(self, content: str, keywords: List[str]) -> float:
        """키워드 기반 관련성을 평가합니다.
        
        Args:
            content: 평가할 콘텐츠
            keywords: 관련성 평가 키워드 목록
            
        Returns:
            관련성 점수 (0.0 ~ 1.0)
        """
        pass
    
    @abstractmethod
    async def evaluate_sentiment(self, content: str) -> float:
        """감정을 평가합니다.
        
        Args:
            content: 평가할 콘텐츠
            
        Returns:
            감정 점수 (-1.0 ~ 1.0, 음수는 부정적, 양수는 긍정적)
        """
        pass
