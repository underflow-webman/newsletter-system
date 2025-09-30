"""Evaluation services - 평가 서비스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import EvaluationResult, EvaluationSession, EvaluationStatus
from .repositories import EvaluationResultRepository, EvaluationSessionRepository


class LLMEvaluationService:
    """LLM 평가 서비스."""
    
    def __init__(self, llm_client, result_repo: EvaluationResultRepository):
        self.llm_client = llm_client
        self.result_repo = result_repo
    
    async def evaluate_post(self, post_id: str, title: str, content: str) -> EvaluationResult:
        """게시글을 평가합니다."""
        text = f"{title}\n{content}"
        
        # LLM으로 관련성 평가
        is_relevant = await self.llm_client.is_relevant(text)
        
        # LLM으로 카테고리 분류
        category = await self.llm_client.classify_category(text)
        
        # 점수 계산
        relevance_score = 0.8 if is_relevant else 0.2
        
        result = EvaluationResult(
            id=f"eval_{datetime.utcnow().timestamp()}",
            post_id=post_id,
            is_relevant=is_relevant,
            category=category,
            relevance_score=relevance_score,
            confidence=0.9,
            details={
                "text_length": len(text),
                "evaluation_method": "llm"
            },
            evaluated_at=datetime.utcnow()
        )
        
        await self.result_repo.save(result)
        return result
    
    async def evaluate_posts_batch(self, posts: List[Dict[str, Any]]) -> List[EvaluationResult]:
        """게시글들을 일괄 평가합니다."""
        results = []
        
        for post in posts:
            try:
                result = await self.evaluate_post(
                    post["id"],
                    post["title"],
                    post["content"]
                )
                results.append(result)
            except Exception as e:
                print(f"Failed to evaluate post {post['id']}: {e}")
        
        return results


class RelevanceEvaluationService:
    """관련성 평가 서비스."""
    
    def __init__(self, llm_client, result_repo: EvaluationResultRepository):
        self.llm_client = llm_client
        self.result_repo = result_repo
        self.keywords = ["통신", "5G", "이통", "KT", "SKT", "LGU", "방통위", "KAIT"]
    
    async def evaluate_relevance(self, post_id: str, title: str, content: str) -> EvaluationResult:
        """게시글의 관련성을 평가합니다."""
        text = f"{title}\n{content}"
        
        # 키워드 매칭
        keywords_found = [kw for kw in self.keywords if kw in text]
        
        # LLM 관련성 평가
        is_relevant = await self.llm_client.is_relevant(text)
        
        # 점수 계산
        keyword_score = min(len(keywords_found) / len(self.keywords), 1.0)
        llm_score = 0.8 if is_relevant else 0.2
        relevance_score = (keyword_score + llm_score) / 2
        
        result = EvaluationResult(
            id=f"relevance_{datetime.utcnow().timestamp()}",
            post_id=post_id,
            is_relevant=is_relevant,
            category="relevance_check",
            relevance_score=relevance_score,
            confidence=0.8,
            details={
                "keywords_found": keywords_found,
                "keyword_score": keyword_score,
                "llm_score": llm_score,
                "evaluation_method": "hybrid"
            },
            evaluated_at=datetime.utcnow()
        )
        
        await self.result_repo.save(result)
        return result
