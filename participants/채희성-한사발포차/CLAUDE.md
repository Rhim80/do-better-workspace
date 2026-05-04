# CLAUDE.md — 채희성 (한사발포차)

> 난로회 AX Bootcamp 2026-05-04~05 / Day 1·2 본인 워크스페이스
> 클론 후 이 파일을 do-better-workspace/CLAUDE.md로 복사:
> `cp participants/채희성-한사발포차/CLAUDE.md ./CLAUDE.md`

## 본인 정보 (사전 입력)

- **이름**: 채희성
- **브랜드**: 한사발포차
- **카테고리**: 한식·주점 (포차)
- **법인 수**: 3+ (난로회 공통 프로필)
- **현장 관리자**: 별도 / 본인은 기획·대표 업무 수행
- **향후 계획**: 프랜차이즈 진출 검토

## 본인 매장 결 (본인이 채움 — 첫날 11:30~12:30)

- 매장 수:
- 본점 위치 (행정동):
- 평수:
- 객단가:
- 운영시간 (심야 영업?):
- 주요 페르소나:
- 향후 출점 후보 상권:

## 도메인 결 — 포차/주점

- 심야·해장 페르소나(P04) 강한 결 — 22:00~04:00 주력
- 주류 매출 비중 + 안주 회전율 핵심
- 데이트·친구모임(P03) 페르소나도 비중 있음 (저녁 1차)
- 운영시간대 매칭 (Rhythm Layer): 심야 시간대 zone의 생활인구 분포 핵심

## 부트캠프 결

- **Day 1 (5/4)**: 마인드셋 → 환경 세팅 → 워크스페이스 클론 → CLAUDE.md 개인화 → personal-context.md 작성 → 진행자 시연(13:30) → 본인 케이스 라이브 분석
- **Day 2 (5/5)**: 본인 도메인 도구 제작·배포

## Claude Code 사용 가이드

> 명령어는 영문, 의미는 한글로 외우세요.

1. `store-interview` — **내 매장 인터뷰** (AI가 단계별로 묻고 personal-context.md 자동 작성)
   - 포차/주점 결: 심야 운영시간(22~04시) · 주류 매출 비중 · 해장 페르소나(P04) 강조
2. `zone-diagnosis {본인_zone}` — **내 자리 진단** (지금 상권 어떤 상태?)
3. `entry-verdict {후보_zone}` — **새 자리 판정** (심야 인구 매칭 핵심)
4. 보조 스킬 (entry-verdict가 자동 호출):
   - `persona-match` — **내 손님 결 맞춤** (그 동네에 내 손님 있나? — 심야 시간대 결 핵심)
   - `competitive-pressure` — **경쟁 압력 점수** (거기 얼마나 빡센가?)
   - `concept-fit` — **객단가·콘셉트 적합도** (내 가격대 맞나?)
5. `zone-report` — **한 페이지 카드 출력** (PDF로 뽑기)

## 참고 파일

- `50-resources/data/personal-context-imicoffee.md` — 진행자 시연 예시
- `50-resources/data/scenarios/scenario-imicoffee-expansion.md` — 시연 흐름
- `50-resources/data/zone-cache/{홍대입구,한남동,성수동,압구정동}.json` — 시연 캐시 (홍대 심야 인구 결 참고)
- `.claude/skills/zone-diagnosis/SKILL.md` · `entry-verdict/SKILL.md`

## Day 2 도구 제작 후보 (방향 예시)

- 심야 매출·주류 비중 대시보드
- 시간대별 페르소나 분석 (1차·2차·해장)
- 주류·안주 페어링 분석
- 다매장 야간 운영 모니터링
