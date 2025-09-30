"""Newsletter use cases - 뉴스레터 유즈케이스들."""

from __future__ import annotations

from typing import List, Dict, Any
from datetime import datetime
from .entities import Newsletter, NewsletterItem
from .services import NewsletterService, TemplateService
from .repositories import NewsletterRepository, SubscriberRepository


class CreateNewsletterUseCase:
    """뉴스레터 생성 유즈케이스."""
    
    def __init__(self, newsletter_service: NewsletterService):
        self.newsletter_service = newsletter_service
    
    async def execute(self, items: List[Dict[str, Any]], title: str) -> Newsletter:
        """뉴스레터를 생성합니다."""
        # 데이터를 NewsletterItem으로 변환
        newsletter_items = [
            NewsletterItem(
                id=f"item_{i}",
                title=item["title"],
                content=item["content"],
                source=item["source"],
                url=item["url"],
                category=item.get("category", "general"),
                relevance_score=item.get("relevance_score", 0.0),
                created_at=datetime.utcnow()
            )
            for i, item in enumerate(items)
        ]
        
        return await self.newsletter_service.create_newsletter(newsletter_items, title)


class SendNewsletterUseCase:
    """뉴스레터 발송 유즈케이스."""
    
    def __init__(self, newsletter_service: NewsletterService, template_service: TemplateService, email_sender):
        self.newsletter_service = newsletter_service
        self.template_service = template_service
        self.email_sender = email_sender
    
    async def execute(self, newsletter_id: str, recipients: List[str]) -> Dict[str, Any]:
        """뉴스레터를 발송합니다."""
        # 뉴스레터 조회
        newsletter = await self.newsletter_service.get_newsletter(newsletter_id)
        if not newsletter:
            raise ValueError(f"Newsletter {newsletter_id} not found")
        
        # 템플릿 렌더링
        html_content = await self.template_service.render_newsletter_template(newsletter)
        
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
        
        # 상태 업데이트
        await self.newsletter_service.newsletter_repo.update_status(newsletter_id, "sent")
        
        return {
            "newsletter_id": newsletter_id,
            "total_recipients": len(recipients),
            "successful_sends": sum(1 for r in results if r["success"]),
            "failed_sends": sum(1 for r in results if not r["success"]),
            "results": results
        }


class DailyNewsletterUseCase:
    """일일 뉴스레터 생성 및 발송 유즈케이스 - 시스템의 메인 워크플로우."""
    
    def __init__(
        self,
        newsletter_service: NewsletterService,
        template_service: TemplateService,
        crawl_community_use_case=None,
        crawl_news_use_case=None,
        crawl_government_use_case=None,
        evaluate_posts_use_case=None,
        email_sender=None
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
        
        # 1단계: 크롤링 (Mock 데이터 사용)
        print("📥 1단계: 데이터 크롤링")
        crawled_posts = await self._crawl_all_sources()
        print(f"✅ 총 {len(crawled_posts)}개 게시글 크롤링 완료")
        
        # 2단계: LLM 평가 (Mock 데이터 사용)
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
        """모든 소스에서 데이터를 크롤링합니다 (Mock 데이터)."""
        # Mock 데이터 반환
        return [
            {
                "id": "mock_1",
                "title": "통신 관련 뉴스 1",
                "content": "5G 기술 발전에 대한 내용입니다.",
                "source": "mock_news",
                "url": "https://example.com/news1",
                "author": "기자1",
                "views": 100,
                "likes": 5,
                "comments": 2
            },
            {
                "id": "mock_2", 
                "title": "SKT 신제품 발표",
                "content": "SKT에서 새로운 통신 서비스를 발표했습니다.",
                "source": "mock_news",
                "url": "https://example.com/news2",
                "author": "기자2",
                "views": 150,
                "likes": 8,
                "comments": 3
            }
        ]
    
    async def _evaluate_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """게시글들을 LLM으로 평가합니다 (Mock 평가)."""
        # Mock 평가 결과 반환
        for post in posts:
            post["relevance_score"] = 0.8  # Mock 관련성 점수
            post["category"] = "통신"  # Mock 카테고리
        return posts
    
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
        
        # Mock 이메일 발송 결과
        return {
            "total_recipients": 1,
            "successful_sends": 1,
            "failed_sends": 0,
            "results": [{
                "recipient": "test@example.com",
                "success": True,
                "message_id": "mock_message_id"
            }]
        }