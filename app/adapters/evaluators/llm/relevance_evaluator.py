"""Relevance evaluator - 관련성 평가 전용."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RelevanceResult:
    """관련성 평가 결과."""
    post_id: str
    is_relevant: bool
    confidence: float
    keywords_found: List[str]
    evaluated_at: datetime


class RelevanceEvaluator:
    """관련성 평가자 - 매우 직관적."""
    
    def __init__(self, llm_service):
        self.llm = llm_service
        self.keywords = ["통신", "5G", "이통", "KT", "SKT", "LGU", "방통위", "KAIT"]
    
    async def evaluate_relevance(self, posts: List[Dict[str, Any]]) -> List[RelevanceResult]:
        """게시글들의 관련성을 평가합니다."""
        results = []
        
        for post in posts:
            text = post["title"] + " " + post["content"]
            
            # 키워드 매칭
            keywords_found = [kw for kw in self.keywords if kw in text]
            
            # LLM 관련성 평가
            is_relevant = await self.llm.is_relevant(text)
            
            # 신뢰도 계산
            confidence = 0.9 if keywords_found else 0.7
            
            results.append(RelevanceResult(
                post_id=post.get("id", "unknown"),
                is_relevant=is_relevant,
                confidence=confidence,
                keywords_found=keywords_found,
                evaluated_at=datetime.utcnow()
            ))
        
        return results
