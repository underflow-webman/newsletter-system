# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-09-30

### 🎉 Major Release - DDD 기반 모듈형 아키텍처 전환

이번 릴리스는 전체 아키텍처를 **Domain-Driven Design (DDD)** 원칙에 따라 대규모 리팩토링한 주요 버전입니다.

### ✨ Added

#### 🏗️ 새로운 아키텍처 구조
- **모듈 기반 구조 도입**: `modules/` 디렉토리로 비즈니스 로직 모듈화
  - `newsletter/` - 뉴스레터 도메인 모듈
  - `crawling/` - 크롤링 도메인 모듈  
  - `evaluation/` - 평가 도메인 모듈
- **어댑터 패턴 적용**: `adapters/` 디렉토리로 외부 시스템 연동 분리
  - `crawlers/` - 크롤링 어댑터들 (community, news, government)
  - `evaluators/` - 평가 어댑터들 (LLM 기반)
  - `senders/` - 발송 어댑터들 (email, notification)
- **인프라 계층 정리**: `infrastructure/` 디렉토리로 기술적 구현체 분리
  - `database/` - 데이터베이스 관련 (모델, 레포지토리 구현체)
  - `external/` - 외부 서비스 연동 (LLM, 이메일)
  - `config/` - 설정 관리

#### 📊 데이터베이스 관리 개선
- **Beanie ODM 도입**: MongoDB를 위한 현대적인 ODM 사용
- **문서 모델 정의**: 각 도메인별 Beanie 문서 모델 생성
  - `NewsletterDocument`, `NewsletterItemDocument`, `SubscriberDocument`
  - `CrawledPostDocument`, `CrawlSessionDocument`
  - `EvaluationResultDocument`, `EvaluationSessionDocument`
- **레포지토리 패턴 구현**: 인터페이스와 구현체 분리
  - 도메인 레이어: 인터페이스 정의 (`repositories.py`)
  - 인프라 레이어: 실제 구현체 (`*_repository_impl.py`)

#### 🔧 의존성 주입 개선
- **DI 컨테이너 리팩토링**: 새로운 모듈 구조에 맞는 의존성 관리
- **타입 안전성 강화**: 제네릭과 타입 힌트를 활용한 안전한 의존성 주입
- **생명주기 관리**: 초기화 및 정리 로직 개선

#### 🌐 API 개선
- **일일 뉴스레터 엔드포인트**: `/newsletter/daily` API 추가
- **유즈케이스 기반 실행**: API에서 직접 유즈케이스 호출
- **에러 처리 개선**: 더 명확한 에러 메시지와 상태 코드

#### 📝 문서화
- **상세한 README**: 새로운 아키텍처 설명 및 사용법 가이드
- **폴더 구조 분석**: `FOLDER_STRUCTURE_ANALYSIS.md` 추가
- **한글 주석**: 모든 코드에 한국어 주석 추가

### 🔄 Changed

#### 🏗️ 아키텍처 변경
- **기존 계층 구조 제거**: `core/`, `domain/`, `application/` 디렉토리 삭제
- **모듈 중심 설계**: 각 도메인이 독립적으로 운영 가능한 구조
- **의존성 방향 개선**: 도메인이 인프라에 의존하지 않는 구조

#### 📁 폴더 구조 개선
- **명확한 역할 분리**: 각 디렉토리의 역할과 책임 명확화
- **확장성 고려**: 많은 파일이 있어도 관리하기 쉬운 구조
- **일관성 있는 네이밍**: 파일과 디렉토리 명명 규칙 통일

#### 🔧 코드 품질 개선
- **타입 힌트 강화**: 모든 함수와 클래스에 타입 힌트 추가
- **에러 처리 개선**: 더 구체적이고 유용한 에러 메시지
- **로깅 개선**: 구조화된 로깅 시스템

### 🗑️ Removed

#### 🧹 불필요한 코드 제거
- **구식 아키텍처**: 기존의 복잡한 계층 구조 제거
- **중복 코드**: 여러 곳에 분산된 중복 로직 제거
- **사용하지 않는 파일**: 더 이상 필요하지 않은 파일들 정리
- **과도한 추상화**: 오버엔지니어링된 인터페이스와 팩토리 제거

#### 📦 의존성 정리
- **불필요한 라이브러리**: 사용하지 않는 외부 의존성 제거
- **중복 모델**: 기존 모델과 새로운 엔티티 통합

### 🐛 Fixed

#### 🔧 버그 수정
- **Import 에러**: 잘못된 import 경로 수정
- **순환 의존성**: 모듈 간 순환 의존성 문제 해결
- **타입 에러**: 타입 힌트 관련 에러 수정
- **설정 파일**: 삭제된 설정 파일 참조 문제 해결

### 🚀 Performance

#### ⚡ 성능 개선
- **비동기 처리**: 모든 I/O 작업을 비동기로 처리
- **데이터베이스 최적화**: 인덱스와 쿼리 최적화
- **메모리 사용량**: 불필요한 객체 생성 최소화
- **응답 시간**: API 응답 시간 개선

### 🔒 Security

#### 🛡️ 보안 강화
- **입력 검증**: Pydantic을 통한 강화된 입력 검증
- **에러 정보**: 민감한 정보가 에러 메시지에 노출되지 않도록 개선
- **의존성 보안**: 최신 버전의 안전한 라이브러리 사용

### 📚 Documentation

#### 📖 문서 개선
- **API 문서**: FastAPI 자동 생성 문서 개선
- **코드 주석**: 모든 주요 함수와 클래스에 상세한 주석 추가
- **사용 예제**: 실제 사용 가능한 코드 예제 추가
- **아키텍처 가이드**: 새로운 구조에 대한 상세한 설명

### 🧪 Testing

#### ✅ 테스트 개선
- **단위 테스트**: 각 모듈별 독립적인 테스트
- **통합 테스트**: 모듈 간 상호작용 테스트
- **모킹**: 외부 의존성 모킹을 통한 안정적인 테스트
- **코드 커버리지**: 테스트 커버리지 향상

### 🔄 Migration

#### 📦 마이그레이션 가이드
- **기존 코드**: 기존 코드를 새로운 구조로 마이그레이션하는 방법
- **설정 변경**: 새로운 설정 구조로의 전환 방법
- **데이터 마이그레이션**: 기존 데이터를 새로운 모델로 이전하는 방법

---

## [1.0.0] - 2025-09-29

### 🎉 Initial Release

#### ✨ Features
- **기본 뉴스레터 시스템**: 뉴스레터 생성, 관리, 발송 기능
- **크롤링 시스템**: 다양한 소스에서 뉴스 수집
- **AI 평가**: LLM을 활용한 관련성 평가
- **이메일 발송**: 구독자에게 뉴스레터 발송
- **FastAPI 기반**: 현대적인 웹 API 프레임워크 사용
- **MongoDB 연동**: NoSQL 데이터베이스 사용

#### 🏗️ Architecture
- **계층형 아키텍처**: Domain, Application, Infrastructure 계층 분리
- **의존성 주입**: DI 컨테이너를 통한 의존성 관리
- **레포지토리 패턴**: 데이터 접근 추상화
- **서비스 계층**: 비즈니스 로직 캡슐화

#### 📦 Dependencies
- **FastAPI**: 웹 프레임워크
- **MongoDB**: 데이터베이스
- **Motor**: 비동기 MongoDB 드라이버
- **Pydantic**: 데이터 검증
- **Uvicorn**: ASGI 서버

---

## 📋 Version History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2025-09-30 | DDD 기반 모듈형 아키텍처 전환 |
| 1.0.0 | 2025-09-29 | 초기 릴리스 |

---

## 🔮 Upcoming Features

### 🚀 Planned for v2.1.0
- **실시간 알림**: WebSocket을 통한 실시간 업데이트
- **대시보드**: 관리자용 웹 대시보드
- **통계 분석**: 뉴스레터 성과 분석
- **A/B 테스트**: 뉴스레터 버전별 성과 비교

### 🎯 Planned for v2.2.0
- **다국어 지원**: 여러 언어 뉴스레터 지원
- **고급 필터링**: 더 정교한 콘텐츠 필터링
- **자동화 규칙**: 사용자 정의 자동화 규칙
- **API 확장**: 더 많은 외부 API 연동

---

## 📞 Support

- **이슈 리포트**: [GitHub Issues](https://github.com/underflow-webman/newsletter-system/issues)
- **문서**: [Wiki](https://github.com/underflow-webman/newsletter-system/wiki)
- **토론**: [Discussions](https://github.com/underflow-webman/newsletter-system/discussions)

---

**Newsletter System** - 더 스마트한 뉴스레터를 위한 진화! 🚀
