"""LLM evaluator - LLM 평가 전용."""

from __future__ import annotations

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EvaluationResult:
    """평가 결과."""
    post_id: str
    is_relevant: bool
    category: str
    score: float
    evaluated_at: datetime


class LLMEvaluator:
    """LLM 평가자 - 매우 직관적."""
    
    def __init__(self, llm_service):
        self.llm = llm_service
    
    async def evaluate_posts(self, posts: List[Dict[str, Any]]) -> List[EvaluationResult]:
        """게시글들을 평가합니다."""
        results = []
        
        for post in posts:
            # LLM으로 관련성 평가
            is_relevant = await self.llm.is_relevant(post["title"] + " " + post["content"])
            
            # LLM으로 카테고리 분류
            category = await self.llm.classify_category(post["title"] + " " + post["content"])
            
            # 점수 계산
            score = 0.8 if is_relevant else 0.2
            
            results.append(EvaluationResult(
                post_id=post.get("id", "unknown"),
                is_relevant=is_relevant,
                category=category,
                score=score,
                evaluated_at=datetime.utcnow()
            ))
        
        return results
