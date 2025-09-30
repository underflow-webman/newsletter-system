# 뉴스레터 시스템 - 매우 직관적

## 🎯 시스템 개요

**매우 직관적이고 심플한** 뉴스레터 시스템입니다.

## 📁 폴더 구조 (매우 직관적)

```
app/
├── main_simple.py          # 메인 실행 파일
├── crawlers/               # 크롤링 전용
│   ├── ppomppu.py         # 뽐뿌 크롤러
│   ├── ruliweb.py         # 루리웹 크롤러
│   └── clien.py           # 클리앙 크롤러
├── evaluators/             # LLM 평가 전용
│   ├── llm_evaluator.py   # LLM 평가자
│   └── relevance_evaluator.py  # 관련성 평가자
├── senders/                # 이메일 발송 전용
│   ├── email_sender.py    # 이메일 발송자
│   └── newsletter_sender.py  # 뉴스레터 발송자
├── core/                   # 핵심 워크플로우
│   └── workflow.py        # 메인 워크플로우
└── infrastructure/         # 인프라 (DB, 외부 서비스)
    ├── repositories/       # 데이터 저장소
    ├── llm/               # LLM 서비스
    └── email/             # 이메일 서비스
```

## 🚀 사용법 (매우 간단)

### 1. 실행
```bash
python app/main_simple.py
```

### 2. 워크플로우
1. **크롤링**: `crawlers/` 폴더의 크롤러들이 데이터 수집
2. **평가**: `evaluators/` 폴더의 평가자들이 LLM으로 데이터 평가
3. **발송**: `senders/` 폴더의 발송자들이 이메일 발송

## 🔧 새 사이트 추가 (매우 간단)

### 1. 크롤러 추가
```python
# app/crawlers/new_site.py
class NewSiteCrawler:
    def __init__(self):
        self.base_url = "https://newsite.com"
    
    async def crawl_hot_posts(self):
        # 크롤링 로직
        pass
```

### 2. __init__.py에 추가
```python
# app/crawlers/__init__.py
from .new_site import NewSiteCrawler
```

## 🎯 핵심 원칙

1. **직관적**: 폴더명만 봐도 역할을 알 수 있음
2. **심플**: 불필요한 추상화 없음
3. **명확**: 각 파일의 역할이 명확함
4. **확장**: 새 기능 추가가 쉬움

## 📝 주요 특징

- **크롤링**: 사이트별 독립 크롤러
- **평가**: LLM 기반 자동 평가
- **발송**: 이메일 자동 발송
- **워크플로우**: 명확한 3단계 프로세스
