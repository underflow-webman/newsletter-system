"""Evaluation use cases - 평가 유즈케이스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import EvaluationResult, EvaluationSession, EvaluationStatus
from .services import LLMEvaluationService, RelevanceEvaluationService
from .repositories import EvaluationResultRepository, EvaluationSessionRepository


class EvaluatePostsUseCase:
    """게시글 평가 유즈케이스."""
    
    def __init__(self, llm_service: LLMEvaluationService, session_repo: EvaluationSessionRepository):
        self.llm_service = llm_service
        self.session_repo = session_repo
    
    async def execute(self, posts: List[Dict[str, Any]]) -> List[EvaluationResult]:
        """게시글들을 평가합니다."""
        # 평가 세션 시작
        session = EvaluationSession(
            id=f"eval_session_{datetime.utcnow().timestamp()}",
            total_posts=len(posts),
            evaluated_posts=0,
            relevant_posts=0,
            irrelevant_posts=0,
            status=EvaluationStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None
        )
        
        await self.session_repo.save(session)
        
        try:
            # 게시글들 평가
            results = await self.llm_service.evaluate_posts_batch(posts)
            
            # 세션 통계 업데이트
            session.evaluated_posts = len(results)
            session.relevant_posts = sum(1 for r in results if r.is_relevant)
            session.irrelevant_posts = sum(1 for r in results if not r.is_relevant)
            session.status = EvaluationStatus.COMPLETED
            session.completed_at = datetime.utcnow()
            
            await self.session_repo.save(session)
            
            return results
            
        except Exception as e:
            # 세션 실패
            session.status = EvaluationStatus.FAILED
            session.error_message = str(e)
            session.completed_at = datetime.utcnow()
            await self.session_repo.save(session)
            raise


class EvaluateRelevanceUseCase:
    """관련성 평가 유즈케이스."""
    
    def __init__(self, relevance_service: RelevanceEvaluationService, session_repo: EvaluationSessionRepository):
        self.relevance_service = relevance_service
        self.session_repo = session_repo
    
    async def execute(self, posts: List[Dict[str, Any]]) -> List[EvaluationResult]:
        """게시글들의 관련성을 평가합니다."""
        # 평가 세션 시작
        session = EvaluationSession(
            id=f"relevance_session_{datetime.utcnow().timestamp()}",
            total_posts=len(posts),
            evaluated_posts=0,
            relevant_posts=0,
            irrelevant_posts=0,
            status=EvaluationStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None
        )
        
        await self.session_repo.save(session)
        
        try:
            results = []
            for post in posts:
                try:
                    result = await self.relevance_service.evaluate_relevance(
                        post["id"],
                        post["title"],
                        post["content"]
                    )
                    results.append(result)
                except Exception as e:
                    print(f"Failed to evaluate relevance for post {post['id']}: {e}")
            
            # 세션 통계 업데이트
            session.evaluated_posts = len(results)
            session.relevant_posts = sum(1 for r in results if r.is_relevant)
            session.irrelevant_posts = sum(1 for r in results if not r.is_relevant)
            session.status = EvaluationStatus.COMPLETED
            session.completed_at = datetime.utcnow()
            
            await self.session_repo.save(session)
            
            return results
            
        except Exception as e:
            # 세션 실패
            session.status = EvaluationStatus.FAILED
            session.error_message = str(e)
            session.completed_at = datetime.utcnow()
            await self.session_repo.save(session)
            raise
