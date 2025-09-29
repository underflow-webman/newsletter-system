# 2025-09-29 DDD 기반 뉴스레터 시스템 리팩토링

## 개요
- DDD(Domain Driven Design) 원칙 적용
- 구독자/캠페인 시스템 제거 (단일 관리자 발송)
- 계층형 크롤러 구조 도입
- 확장 가능한 아키텍처 설계

## 주요 변경사항

### 1. DDD 계층 구조 도입
```
app/
├── domain/           # 도메인 계층
│   ├── entities.py   # 엔티티/값객체
│   └── ports.py      # 인터페이스 정의
├── application/      # 애플리케이션 계층
│   ├── dtos.py       # DTO 정의
│   └── use_cases/    # 유스케이스 패키지
│       ├── crawl_and_draft.py
│       └── batch_crawl.py
├── infrastructure/   # 인프라 계층
│   ├── crawlers/     # 크롤러 구현체
│   ├── llm.py        # LLM 서비스
│   ├── repositories.py
│   ├── email.py
│   └── di.py         # DI 컨테이너
└── api/             # 프레젠테이션 계층
    ├── admin.py      # 관리자 엔드포인트
    └── newsletter.py # 뉴스레터 CRUD
```

### 2. 제거된 기능
- **구독자 시스템**: `subscribers.py`, `subscriber_service.py`, `subscriber.py` 삭제
- **캠페인 시스템**: `campaigns.py`, `campaign_service.py`, `campaign.py` 삭제
- **이유**: 단일 관리자 발송, 수신자 관리는 다우오피스 API 사용

### 3. 새로 추가된 기능

#### 도메인 포트 (인터페이스)
- `ICrawler`: 사이트별 크롤러 전략
- `ILLMService`: LLM 벤더/모델 추상화
- `INewsRepository`: 뉴스 데이터 저장소 추상화
- `IEmailSender`: 이메일 발송 어댑터

#### 계층형 크롤러 구조
```
crawlers/
├── base.py                    # 기본 샘플 크롤러
├── community.py               # 커뮤니티 크롤러
├── etnews.py                  # 전자신문 크롤러
└── gov_broadcast_commission.py # 방통위 크롤러
```

#### 유스케이스
- `CrawlAndDraftNewsletterUseCase`: 크롤링 → 필터링 → 요약 → 초안 생성
- `BatchCrawlUseCase`: 계층형 일괄 크롤링

#### 관리자 API
- `POST /api/v1/admin/crawl_manual`: 수동 크롤링 + 초안 생성
- `POST /api/v1/admin/batch_crawl`: 계층형 일괄 크롤링
- `POST /api/v1/admin/send_newsletter_manual`: 테스트 발송

### 4. 확장성 고려사항

#### 크롤러 확장
- 각 사이트별로 독립적인 크롤러 클래스
- `options` 파라미터로 페이지 수, 날짜 범위 등 설정 가능
- DI 컨테이너에서 그룹 → 소스 → 타겟키 매핑

#### LLM 교체
- `MockLLM` → 실제 Claude/Gemini API로 교체 가능
- 인터페이스 기반으로 벤더 독립적

#### 저장소 교체
- `InMemoryNewsRepository` → MongoDB 기반 구현으로 교체 가능

### 5. 사용 예시

#### 계층형 크롤링 요청
```json
POST /api/v1/admin/batch_crawl
{
  "sources": {
    "community": {
      "ppomppu": {
        "mobile": { "pages": 2, "days": 3, "limit": 50 }
      }
    },
    "news": {
      "etnews": {
        "it-telecom": { "pages": 1, "days": 1, "limit": 20 }
      }
    },
    "gov": {
      "kcc": {
        "press": { "pages": 1, "days": 7, "limit": 100 }
      }
    }
  }
}
```

#### 초안 생성 요청
```json
POST /api/v1/admin/crawl_manual
{
  "sources": ["community", "etnews", "gov"],
  "limit_per_source": 5
}
```

## 다음 단계
1. MongoDB 기반 `INewsRepository` 구현
2. Selenium 기반 실제 크롤러 구현
3. 실제 LLM API 연동 (Claude/Gemini)
4. 환경변수 설정 가이드 작성
5. 배치 스케줄링 추가

## 기술 스택
- **백엔드**: FastAPI
- **데이터베이스**: MongoDB (Beanie ODM)
- **크롤링**: Selenium (구현 예정)
- **LLM**: Claude/Gemini (구현 예정)
- **이메일**: 다우오피스 API
- **아키텍처**: DDD + CQRS-lite

## 파일 변경 내역
### 삭제된 파일
- `app/api/campaigns.py`
- `app/api/subscribers.py`
- `app/models/campaign.py`
- `app/models/subscriber.py`
- `app/services/campaign_service.py`
- `app/services/subscriber_service.py`

### 새로 추가된 파일
- `app/domain/entities.py`
- `app/domain/ports.py`
- `app/application/dtos.py`
- `app/application/use_cases/crawl_and_draft.py`
- `app/application/use_cases/batch_crawl.py`
- `app/infrastructure/crawlers/` (패키지)
- `app/infrastructure/llm.py`
- `app/infrastructure/repositories.py`
- `app/infrastructure/email.py`
- `app/infrastructure/di.py`
- `app/api/admin.py`

### 수정된 파일
- `app/api/routes.py`: 구독자/캠페인 라우터 제거
- `app/main.py`: 라우터 등록 수정
- `app/core/database.py`: 모델 초기화 수정
