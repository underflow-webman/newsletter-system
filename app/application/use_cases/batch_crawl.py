from __future__ import annotations

from typing import Dict, Any, List

from app.domain.ports import ICrawler, ILLMService, INewsRepository, CrawlTarget, RawPost
from app.application.dtos import HierarchicalCrawlRequest


class BatchCrawlUseCase:
    """계층적 소스 구조를 따라 일괄 크롤링을 수행."""

    def __init__(
        self,
        crawlers: Dict[str, Dict[str, Dict[str, ICrawler]]],
        repository: INewsRepository,
    ) -> None:
        self._crawlers = crawlers
        self._repository = repository

    async def execute(self, req: HierarchicalCrawlRequest) -> Dict[str, int]:
        saved_total = 0
        for group, sources in req.sources.items():
            for source_name, targets in sources.items():
                for target_key, options in targets.items():
                    crawler = (
                        self._crawlers.get(group, {})
                        .get(source_name, {})
                        .get(target_key)
                    )
                    if not crawler:
                        continue
                    target = CrawlTarget(
                        source_name=f"{group}:{source_name}:{target_key}",
                        base_url="",
                        category=group,
                        limit=options.limit,
                    )
                    posts = await crawler.list_posts(target, options=dict(options))
                    saved_total += await self._repository.save_raw_posts(posts)
        return {"saved": saved_total}


