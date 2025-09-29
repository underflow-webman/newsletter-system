from __future__ import annotations

from typing import Dict, List

from app.domain.ports import ICrawler, ILLMService, INewsRepository, CrawlTarget, RawPost
from app.domain.entities import NewsItem, Category, Summary
from app.application.dtos import CrawlRequest, NewsletterDraftDTO, CategoryNewsDTO


class CrawlAndDraftNewsletterUseCase:
    """크롤링 → 필터 → 중복제거 → 분류/요약 → 초안 작성"""

    def __init__(
        self,
        crawlers: Dict[str, ICrawler],
        llm: ILLMService,
        repository: INewsRepository,
    ) -> None:
        self._crawlers = crawlers
        self._llm = llm
        self._repository = repository

    async def execute(self, req: CrawlRequest) -> NewsletterDraftDTO:
        all_posts: List[RawPost] = []
        for source in req.sources:
            crawler = self._crawlers.get(source)
            if not crawler:
                continue
            target = CrawlTarget(source_name=source, base_url="", category="generic", limit=req.limit_per_source)
            posts = await crawler.list_posts(target)
            all_posts.extend(posts)

        filtered = [p for p in all_posts if (p.title and p.content_snippet)]
        relevant: List[RawPost] = []
        for p in filtered:
            if await self._llm.is_relevant(f"{p.title}\n{p.content_snippet}"):
                relevant.append(p)

        titles = [p.title for p in relevant]
        keep_indices = await self._llm.deduplicate(titles) if relevant else []
        deduped = [relevant[i] for i in keep_indices] if keep_indices else relevant

        categorized: Dict[str, List[NewsItem]] = {}
        for p in deduped:
            category_name = await self._llm.classify_category(f"{p.title}\n{p.content_snippet}")
            try:
                category = Category(category_name)
            except Exception:
                category = Category.OTHER
            summary_text = await self._llm.summarize(p.content_snippet, sentences=3)
            item = NewsItem(
                title=p.title,
                url=p.url,
                source_name=p.source_name,
                category=category,
                summary=Summary(text=summary_text, sentences=3),
                original_excerpt=p.content_snippet,
            )
            categorized.setdefault(category.value, []).append(item)

        cat_dtos: List[CategoryNewsDTO] = []
        for cat, items in categorized.items():
            selected = items[:3]
            cat_dtos.append(
                CategoryNewsDTO(
                    category=cat,
                    items=[
                        {
                            "title": ni.title,
                            "url": ni.url,
                            "summary": ni.summary.text if ni.summary else "",
                            "source": ni.source_name,
                        }
                        for ni in selected
                    ],
                )
            )

        html_sections = []
        for c in cat_dtos:
            block = "".join(
                [
                    f'<li><a href="{it["url"]}">{it["title"]}</a><br/><small>{it["summary"]}</small></li>'
                    for it in c.items
                ]
            )
            html_sections.append(f"<h3>{c.category}</h3><ul>{block}</ul>")
        html = "\n".join(html_sections)

        draft = NewsletterDraftDTO(
            subject="통신시장 주간 뉴스레터(초안)",
            categories=cat_dtos,
            html_content=html,
        )

        await self._repository.save_raw_posts(all_posts)
        await self._repository.save_newsletter_draft(draft.dict())
        return draft


