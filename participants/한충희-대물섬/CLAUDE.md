# CLAUDE.md — 한충희 (대물섬)

> 난로회 AX Bootcamp 2026-05-04~05 / Day 1·2 본인 워크스페이스
> 클론 후 이 파일을 do-better-workspace/CLAUDE.md로 복사:
> `cp participants/한충희-대물섬/CLAUDE.md ./CLAUDE.md`

## 본인 정보 (사전 입력)

- **이름**: 한충희
- **브랜드**: 대물섬
- **카테고리**: 한식
- **법인 수**: 3+ (난로회 공통 프로필)
- **현장 관리자**: 별도 / 본인은 기획·대표 업무 수행
- **향후 계획**: 프랜차이즈 진출 검토

## 본인 매장 결 (본인이 채움 — 첫날 11:30~12:30)

- 매장 수:
- 본점 위치 (행정동):
- 평수:
- 객단가:
- 운영시간:
- 주요 페르소나:
- 향후 출점 후보 상권 (1-3곳):

## 부트캠프 결

- **Day 1 (5/4)**: 마인드셋 → 환경 세팅 → 워크스페이스 클론 → CLAUDE.md 개인화 → personal-context.md 작성 → 진행자 시연(13:30) → 본인 케이스 라이브 분석
- **Day 2 (5/5)**: 본인 도메인 도구 제작·배포

## Claude Code 사용 가이드

> 명령어는 영문, 의미는 한글로 외우세요.

1. `store-interview` — **내 매장 인터뷰** (AI가 단계별로 묻고 personal-context.md 자동 작성)
   - 직접 채우셔도 OK, 막히면 이 스킬 호출
2. `zone-diagnosis {본인_zone}` — **내 자리 진단** (지금 상권 어떤 상태?)
3. `entry-verdict {후보_zone}` — **새 자리 판정** (Go / 조건부 / 안됨)
4. 보조 스킬 (entry-verdict가 자동 호출):
   - `persona-match` — **내 손님 결 맞춤** (그 동네에 내 손님 있나?)
   - `competitive-pressure` — **경쟁 압력 점수** (거기 얼마나 빡센가?)
   - `concept-fit` — **객단가·콘셉트 적합도** (내 가격대 맞나?)
5. `zone-report` — **한 페이지 카드 출력** (PDF로 뽑기)

## 참고 파일

- `50-resources/data/personal-context-imicoffee.md` — 진행자 시연 예시
- `50-resources/data/scenarios/scenario-imicoffee-expansion.md` — 시연 흐름
- `50-resources/data/zone-cache/{홍대입구,한남동,성수동,압구정동}.json` — 시연 캐시
- `.claude/skills/zone-diagnosis/SKILL.md` · `entry-verdict/SKILL.md`

## Day 2 도구 제작 후보 (방향 예시)

- 본인 매장 매출 대시보드 (시간대별·메뉴별)
- 다매장 통합 운영 모니터링 (본점·분점 비교)
- POS+배달앱 통합 (네이버·배민·쿠팡이츠)
- 메뉴 회전율·BEP 추적

## 도구 만들 때 쓸 수 있는 스킬·에이전트

> Day 2 본인 도구 제작 시 호출.

- `webapp-prd` — **웹앱/대시보드 PRD 대화형 생성** (사장님이 만들고 싶은 도구를 AI가 PRD로 정리)
- `dashboard-prd` — 대시보드 전용 PRD (KPI·차트·필터 구조)
- `analysis-worker` — 데이터 분석 보조 에이전트 (트렌드·SWOT·페르소나 분석)
- `csv-clean` / `excel-to-csv` — POS·매출 raw 데이터 정리
- `transcript-organizer` — 직원 미팅·고객 인터뷰 녹취 정리
- `notion-handler` — 결과를 Notion DB로 저장
- `web-crawler-ocr` — 경쟁사 메뉴·리뷰·이미지 크롤링
