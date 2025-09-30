# 폴더 구조 분석 및 개선안

## 🔍 현재 구조의 문제점

### 1. 중복된 역할
- `crawlers/` vs `modules/crawling/` - 크롤링 관련 중복
- `evaluators/` vs `modules/evaluation/` - 평가 관련 중복
- `senders/` vs `modules/newsletter/` - 발송 관련 중복
- `services/` vs `modules/*/services.py` - 서비스 중복

### 2. 일관성 없는 구조
- `modules/` 안에는 DDD 구조 (entities, repositories, services, use_cases)
- `crawlers/`, `evaluators/`, `senders/`는 단순 구현체들만
- `infrastructure/`는 기술적 구현체들

### 3. 역할이 모호한 폴더들
- `core/` - 설정과 DB가 섞여있음
- `services/` - 모듈별 서비스와 혼재
- `api/` - 단순한 HTTP 엔드포인트

## 🎯 개선된 폴더 구조

```
app/
├── modules/                    # 📦 비즈니스 모듈들 (DDD 구조)
│   ├── newsletter/            # 뉴스레터 모듈
│   │   ├── entities.py        # Newsletter, NewsletterItem, Subscriber
│   │   ├── repositories.py    # NewsletterRepository, SubscriberRepository
│   │   ├── services.py        # NewsletterService, TemplateService
│   │   └── use_cases/         # 비즈니스 유즈케이스들
│   │       ├── daily_newsletter_use_case.py
│   │       ├── create_newsletter_use_case.py
│   │       └── send_newsletter_use_case.py
│   ├── crawling/              # 크롤링 모듈
│   │   ├── entities.py        # CrawledPost, CrawlSession
│   │   ├── repositories.py    # CrawledPostRepository, CrawlSessionRepository
│   │   ├── services.py        # CrawlingService, DataExtractionService
│   │   └── use_cases/         # 크롤링 유즈케이스들
│   │       ├── crawl_community_use_case.py
│   │       ├── crawl_news_use_case.py
│   │       └── crawl_government_use_case.py
│   └── evaluation/            # 평가 모듈
│       ├── entities.py        # EvaluationResult, EvaluationSession
│       ├── repositories.py    # EvaluationResultRepository, EvaluationSessionRepository
│       ├── services.py        # LLMEvaluationService, RelevanceEvaluationService
│       └── use_cases/         # 평가 유즈케이스들
│           ├── evaluate_posts_use_case.py
│           └── evaluate_relevance_use_case.py
├── adapters/                  # 🔌 외부 시스템 어댑터들
│   ├── crawlers/              # 크롤링 어댑터들
│   │   ├── community/         # 커뮤니티 크롤러들
│   │   │   ├── ppomppu_crawler.py
│   │   │   ├── ruliweb_crawler.py
│   │   │   └── clien_crawler.py
│   │   ├── news/              # 뉴스 크롤러들
│   │   │   ├── etnews_crawler.py
│   │   │   └── yonhap_crawler.py
│   │   └── government/        # 정부 크롤러들
│   │       ├── broadcast_commission_crawler.py
│   │       └── kait_crawler.py
│   ├── evaluators/            # 평가 어댑터들
│   │   ├── llm_evaluator.py
│   │   └── relevance_evaluator.py
│   └── senders/               # 발송 어댑터들
│       ├── email_sender.py
│       ├── newsletter_sender.py
│       ├── slack_sender.py
│       └── webhook_sender.py
├── infrastructure/            # 🏗️ 인프라 구현체들
│   ├── database/              # 데이터베이스 관련
│   │   ├── repositories/      # 레포지토리 구현체들
│   │   │   ├── newsletter_repository_impl.py
│   │   │   ├── crawling_repository_impl.py
│   │   │   └── evaluation_repository_impl.py
│   │   └── models/            # DB 모델들
│   │       ├── newsletter_models.py
│   │       ├── crawling_models.py
│   │       └── evaluation_models.py
│   ├── external/              # 외부 서비스 연동
│   │   ├── llm/               # LLM 서비스들
│   │   │   ├── openai_client.py
│   │   │   ├── claude_client.py
│   │   │   └── mock_llm_client.py
│   │   └── email/             # 이메일 서비스들
│   │       ├── sendgrid_client.py
│   │       ├── smtp_client.py
│   │       └── daou_client.py
│   └── config/                # 설정 관련
│       ├── settings.py
│       └── database.py
├── api/                       # 🌐 HTTP API 엔드포인트들
│   ├── v1/                    # API 버전 1
│   │   ├── newsletter.py      # 뉴스레터 API
│   │   ├── crawling.py        # 크롤링 API
│   │   └── evaluation.py      # 평가 API
│   └── dependencies.py        # API 의존성들
└── main.py                    # 🚀 애플리케이션 진입점
```

## 🎯 개선된 구조의 장점

### 1. 명확한 역할 분리
- `modules/` - 비즈니스 로직 (DDD)
- `adapters/` - 외부 시스템 연동
- `infrastructure/` - 기술적 구현체
- `api/` - HTTP 인터페이스

### 2. 일관성 있는 구조
- 모든 모듈이 동일한 DDD 구조
- 어댑터들은 단순한 구현체
- 인프라는 기술적 세부사항

### 3. 확장성
- 새 모듈 추가: `modules/new_module/` 생성
- 새 어댑터 추가: `adapters/new_adapter.py` 생성
- 새 API 추가: `api/v1/new_api.py` 생성

### 4. 테스트 용이성
- 모듈별 독립적 테스트
- 어댑터별 단위 테스트
- API별 통합 테스트
