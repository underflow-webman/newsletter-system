"""일일 뉴스레터 유즈케이스 - 뉴스레터 시스템의 메인 실행 로직."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from ..entities import Newsletter, NewsletterItem
from ..services import NewsletterService, TemplateService
from ...crawling.use_cases import CrawlCommunityUseCase, CrawlNewsUseCase, CrawlGovernmentUseCase
from ...evaluation.use_cases import EvaluatePostsUseCase


class DailyNewsletterUseCase:
    """일일 뉴스레터 생성 및 발송 유즈케이스 - 시스템의 메인 워크플로우."""
    
    def __init__(
        self,
        newsletter_service: NewsletterService,
        template_service: TemplateService,
        crawl_community_use_case: CrawlCommunityUseCase,
        crawl_news_use_case: CrawlNewsUseCase,
        crawl_government_use_case: CrawlGovernmentUseCase,
        evaluate_posts_use_case: EvaluatePostsUseCase,
        email_sender
    ):
        self.newsletter_service = newsletter_service
        self.template_service = template_service
        self.crawl_community_use_case = crawl_community_use_case
        self.crawl_news_use_case = crawl_news_use_case
        self.crawl_government_use_case = crawl_government_use_case
        self.evaluate_posts_use_case = evaluate_posts_use_case
        self.email_sender = email_sender
    
    async def execute(self) -> Dict[str, Any]:
        """일일 뉴스레터를 생성하고 발송합니다."""
        print("🚀 일일 뉴스레터 시스템 시작")
        
        # 1단계: 크롤링
        print("📥 1단계: 데이터 크롤링")
        crawled_posts = await self._crawl_all_sources()
        print(f"✅ 총 {len(crawled_posts)}개 게시글 크롤링 완료")
        
        # 2단계: LLM 평가
        print("🧠 2단계: LLM 평가")
        evaluated_posts = await self._evaluate_posts(crawled_posts)
        print(f"✅ 총 {len(evaluated_posts)}개 게시글 평가 완료")
        
        # 3단계: 뉴스레터 생성
        print("📝 3단계: 뉴스레터 생성")
        newsletter = await self._create_newsletter(evaluated_posts)
        print(f"✅ 뉴스레터 생성 완료: {newsletter.title}")
        
        # 4단계: 이메일 발송
        print("📧 4단계: 이메일 발송")
        send_result = await self._send_newsletter(newsletter)
        print(f"✅ 이메일 발송 완료: {send_result['successful_sends']}명")
        
        print("✅ 일일 뉴스레터 시스템 완료")
        
        return {
            "newsletter_id": newsletter.id,
            "crawled_posts": len(crawled_posts),
            "evaluated_posts": len(evaluated_posts),
            "newsletter_items": len(newsletter.items),
            "send_result": send_result
        }
    
    async def _crawl_all_sources(self) -> List[Dict[str, Any]]:
        """모든 소스에서 데이터를 크롤링합니다."""
        all_posts = []
        
        # 커뮤니티 크롤링
        community_posts = await self.crawl_community_use_case.execute("ppomppu", [])
        all_posts.extend([self._convert_to_dict(post) for post in community_posts])
        
        # 뉴스 크롤링
        news_posts = await self.crawl_news_use_case.execute("etnews", [])
        all_posts.extend([self._convert_to_dict(post) for post in news_posts])
        
        # 정부 크롤링
        government_posts = await self.crawl_government_use_case.execute("broadcast_commission", [])
        all_posts.extend([self._convert_to_dict(post) for post in government_posts])
        
        return all_posts
    
    async def _evaluate_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """게시글들을 LLM으로 평가합니다."""
        return await self.evaluate_posts_use_case.execute(posts)
    
    async def _create_newsletter(self, posts: List[Dict[str, Any]]) -> Newsletter:
        """평가된 게시글들로 뉴스레터를 생성합니다."""
        # 관련성 높은 게시글만 필터링
        relevant_posts = [post for post in posts if post.get("relevance_score", 0) > 0.5]
        
        # NewsletterItem으로 변환
        newsletter_items = [
            NewsletterItem(
                id=f"item_{i}",
                title=post["title"],
                content=post["content"],
                source=post["source"],
                url=post["url"],
                category=post.get("category", "general"),
                relevance_score=post.get("relevance_score", 0.0),
                created_at=datetime.utcnow()
            )
            for i, post in enumerate(relevant_posts)
        ]
        
        # 뉴스레터 생성
        title = f"일일 뉴스레터 - {datetime.utcnow().strftime('%Y년 %m월 %d일')}"
        return await self.newsletter_service.create_newsletter(newsletter_items, title)
    
    async def _send_newsletter(self, newsletter: Newsletter) -> Dict[str, Any]:
        """뉴스레터를 이메일로 발송합니다."""
        # 템플릿 렌더링
        html_content = await self.template_service.render_newsletter_template(newsletter)
        
        # TODO: 실제 구독자 목록 조회
        recipients = ["test@example.com"]  # 임시 구독자 목록
        
        # 이메일 발송
        results = []
        for recipient in recipients:
            try:
                result = await self.email_sender.send_email(
                    to=recipient,
                    subject=newsletter.title,
                    content=html_content
                )
                results.append({
                    "recipient": recipient,
                    "success": True,
                    "message_id": result.get("message_id")
                })
            except Exception as e:
                results.append({
                    "recipient": recipient,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "total_recipients": len(recipients),
            "successful_sends": sum(1 for r in results if r["success"]),
            "failed_sends": sum(1 for r in results if not r["success"]),
            "results": results
        }
    
    def _convert_to_dict(self, post) -> Dict[str, Any]:
        """크롤링된 게시글을 딕셔너리로 변환합니다."""
        return {
            "id": getattr(post, "id", f"post_{datetime.utcnow().timestamp()}"),
            "title": getattr(post, "title", ""),
            "content": getattr(post, "content", ""),
            "source": getattr(post, "source", ""),
            "url": getattr(post, "url", ""),
            "author": getattr(post, "author", ""),
            "views": getattr(post, "views", 0),
            "likes": getattr(post, "likes", 0),
            "comments": getattr(post, "comments", 0)
        }
