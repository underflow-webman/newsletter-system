from __future__ import annotations

from typing import Dict

from app.infrastructure.crawlers import SimpleListCrawler, EtNewsCrawler, CommunityCrawler, GovBroadcastCommissionCrawler
from app.infrastructure.llm import MockLLM
from app.infrastructure.repositories import InMemoryNewsRepository
from app.infrastructure.email import DaouEmailSenderAdapter
from app.services.daou_office_service import daou_office_service


class Container:
    """아주 간단한 DI 컨테이너: 전략/어댑터를 조립하여 주입합니다."""

    def __init__(self) -> None:
        # 2단계: 그룹 → 소스 → 타겟키 레지스트리
        self.crawlers_registry: Dict[str, Dict[str, Dict[str, object]]] = {
            "community": {
                "ppomppu": {
                    "mobile": CommunityCrawler(),
                    "telecom": CommunityCrawler(),
                },
                "ruliweb": {
                    "hot": CommunityCrawler(),
                },
            },
            "news": {
                "etnews": {
                    "it-telecom": EtNewsCrawler(),
                },
            },
            "gov": {
                "kcc": {
                    "press": GovBroadcastCommissionCrawler(),
                },
            },
        }
        self.llm = MockLLM()
        self.repository = InMemoryNewsRepository()
        self.email_sender = DaouEmailSenderAdapter(daou_office_service)


container = Container()


