from __future__ import annotations

from typing import List

from app.domain.ports import ICrawler, CrawlTarget, RawPost


class SimpleListCrawler(ICrawler):
    """
    최소 샘플 크롤러: 고정/샘플 데이터를 반환.
    실제 사용 시, 타겟별 Selenium 로직을 이 클래스 또는 파생 클래스로 구현.
    """

    async def list_posts(self, target: CrawlTarget) -> List[RawPost]:
        sample = [
            RawPost(
                source_name=target.source_name,
                url=f"https://example.com/{i}",
                title=f"{target.source_name} 통신시장 뉴스 {i}",
                content_snippet="5G 투자와 요금제 개편 관련 소식.",
            )
            for i in range(min(target.limit, 5))
        ]
        return sample


