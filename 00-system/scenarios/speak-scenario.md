# 스픽 AX 부트캠프 — 4/16

> **샘플 데이터**: `50-resources/sample-data/speak/`

---

## 참여자

| 이름 | 팀 | 역할 | 하는 일 |
|------|-----|------|---------|
| **백폴** | 피플팀 | APAC 채용 리드 | 한·일·대만 12개 포지션 풀사이클 채용 |
| **황정기** | 채용팀 | APAC Recruiting Coordinator | 인터뷰 스케줄링, 후보자 커뮤니케이션 |
| **이선재** | People Ops | APAC People Ops 리드 | Performance/Comp Cycle, HRBP, 오피스 이전 |
| **이시현** | 피플옵스팀 | APAC People Ops Coordinator | Contractor Lifecycle, 온보딩/오프보딩 |
| **Finance 담당자** | 파이낸스팀 | Finance (APAC) | 메일/슬랙 응대, CRM 검토, billing 처리 |

---

## 상황

**목요일 아침 9시. 성수동.**

백폴이 노트북을 연다. Ashby 탭을 켜고 P0 포지션 5개를 하나씩 훑는다. 어떤 건 잘 가고, 어떤 건 한 달째 같은 자리다. 왜 막혔는지는 모른다. 옆에서 황정기가 "어제 보낸 피드백 요청 또 답 안 왔어" 하고 투덜댄다.

이시현은 Google Sheet를 연다. Contractor 37명. 이번 달에 끝나는 사람이 몇 명인지, 그중 Extension 요청 안 된 건 누군지 — 시트를 수기로 훑고 있다. 30분째다.

건너편에 Finance 담당자가 있다. 3월 CRM을 보며 "Taiwan 쪽 billing 이슈가 유난히 많네"라고 한다. 느낌은 있는데 데이터로 본 적은 없다.

어제 CEO가 Slack에 남긴 메시지 때문에 오늘은 좀 다르다.

> **Connor (CEO)**: APAC team, Q2 plan 전에 3개만 알려줘.
> 1. P0 포지션 중에 target 넘길 위험이 있는 건 어디고, 왜?
> 2. 샌프란 인터뷰어 피드백이 늦어서 APAC 후보자가 느려지고 있나?
> 3. Taiwan entity 세팅하면서 contractor billing이 쌓인 것 같은데 패턴 있어?
>
> **이선재**: 내일 워크숍에서 답 만들자. 데이터 다 모아서.

**(백폴, 속으로)** 원래 이거 하려면 Ashby/Gmail/Calendar 다 열어서 수기 크로스체크. 2~3시간 걸리고 그것도 누락 안고. 오늘은 Claude Code로 해본다.

**(이시현, 속으로)** 내 시트랑 Finance CRM을 contractor_id로 붙여본 적이 한 번도 없다. 오늘 해본다.

---

## 미션 1. P0 포지션, 어디서 막혔나

**담당**: 백폴 · 황정기 · 이선재

> **백폴**: P0 5개 중에 뭐가 진짜 위험한 건지 모르겠어. 후보자가 부족한 건지, 피드백이 안 오는 건지, 내가 놓친 건지.
>
> **황정기**: 나도 매일 아침 Ashby 돌면서 "내 공인 후보자" 찾는데, 5일 넘게 놓친 건 거의 다 빠져.

**쓰는 파일**: `speak_positions_master.csv`, `speak_recruiting_pipeline_2601_2604.csv`, `speak_interview_feedback_2601_2604.csv`

**분석 요청**:
```
@speak_positions_master.csv @speak_recruiting_pipeline_2601_2604.csv @speak_interview_feedback_2601_2604.csv 같이 봐줘.

1. P0 포지션 5개 상태
   - 오픈한 지 며칠 됐는지 (target 60일 넘었는지)
   - 후보자 수와 단계별 분포
   - 내 공인데 5일 넘게 방치된 후보자 몇 명

2. 인터뷰어 피드백 속도
   - 샌프란 vs APAC 평균 제출 소요일
   - 미제출률 비교

3. P0 5개를 Red / Yellow / Green으로 나눠줘.
   Red는 이유까지 (후보자 부족 / 피드백 지연 / 내가 놓침)
```

**추가로 물어볼 만한 것**:
```
@speak_recruiting_pipeline_2601_2604.csv 에서 방치된 후보자 Top 10 뽑아줘.
오늘 바로 연락 돌리게.
```

**도전 과제**:
```
CEO 공유용 HTML 대시보드 만들어줘.
- P0 5개 신호등 (Red/Yellow/Green + 이유)
- 방치 후보자 Top 10 테이블
- 샌프란 vs APAC 피드백 속도 차트
```

---

## 미션 2. Contractor × Billing, 숨은 연결

**담당**: 이시현 · Finance 담당자 · 이선재

> **이시현**: 이번 달 끝나는 contractor 중 Extension 아직 안 된 사람만 깔끔하게 뽑고 싶어.
>
> **Finance**: TW 쪽 billing 이슈가 많다는 느낌은 있는데, 진짜 그런지 데이터로 보고 싶어요.
>
> **이선재**: 이시현 시트랑 Finance CRM을 contractor_id로 붙여본 적이 없어. 오늘 해보자.

**쓰는 파일**: `speak_contractor_lifecycle.csv`, `speak_finance_billing_issues_2601_2604.csv`

**분석 요청 (1단계)**:
```
@speak_contractor_lifecycle.csv 먼저 봐줘.

1. 국가별 현황 (KR/JP/TW)
   - 전체, Active, 30일 안에 끝나는 사람, Extension 요청된 건

2. 이번 달 처리해야 할 사람
   - 30일 안에 끝나는데 Extension도 Offboarding도 시작 안 된 사람
   - 각자 manager에게 보낼 Slack DM 초안까지

3. 진행 중에 멈춰있는 케이스
   - DocuSign 발송했는데 서명 대기
   - 서명 끝났는데 Deel 업로드 안 됨
   - Deel 끝났는데 Tool onboarding 안 됨
```

**분석 요청 (2단계)**:
```
@speak_contractor_lifecycle.csv @speak_finance_billing_issues_2601_2604.csv 교차해서 봐줘.

1. Billing 이슈 국가별 분포 — 어디에 몰려 있어?
2. TW contractor 중 몇 명이 billing 이슈에 엮여 있어?
3. TW에서 자주 나오는 이슈 타입은 뭐야?
   구조적 문제처럼 보여, 일회성이야?
```

**도전 과제**:
```
Contractor 대시보드 HTML로 만들어줘.
- 오늘 할 일 (End date 임박 / 서명 대기 / Deel 업로드 대기)
- 국가 × 상태 매트릭스 (KR/JP/TW)
- Billing 이슈 걸린 contractor 리스트
```

---

## 에필로그

**오후 5시. 결과가 나왔다.**

P0 5개 중 **Red 3개, Yellow 2개**였다. Red 원인이 서로 달랐다.

- **POS-2601-001 (Growth Marketing, Korea)** — 오픈 **97일**, target 한참 넘김. 방치된 후보자 **5명**이 백폴 공이었다. **내가 놓친 것.**
- **POS-2601-002 (Product Designer, APAC)** — 오픈 **93일**. 샌프란 인터뷰어 피드백이 평균 3.1일, 미제출률 11%. **피드백 지연.**
- **POS-2602-003 (Content Marketing, Japan)** — 샌프란 미제출률 **24% (11/45)**. 가장 심함. **피드백 지연.**

샌프란 vs APAC 피드백 속도는 **3.7일 vs 1.4일 (2.6배)**, 미제출률은 **21% vs 5% (4배)**. 느낌이 맞았다.

Contractor 쪽: 30일 안에 끝나는 **4명** 중 **3명이 Extension 미요청**. 최은지(KR, 9일), Miyu Kondo(JP, 1일), 오서연(KR, 19일). 오늘 Slack 돌려야 한다.

TW contractor **13명 중 10명**이 billing 이슈에 연결됐다. "Duplicate invoice" 3건, "Missing billing contact" 3건. 일회성 아니라 **구조적 문제** — Taiwan entity 세팅 전까진 신규 TW 건은 Finance 승인 루프 추가.

> **이선재 → #apac-people-leadership**
> Connor, Q1~Q3 답 정리했어.
> 1. Red 3개 (원인 다 다름), Yellow 2개.
> 2. 샌프란 피드백 3.7일 vs APAC 1.4일. 미제출률 21% vs 5%. 지연 확인.
> 3. TW billing은 구조적. 13명 중 10명 이슈 연결. 이번 주에 Finance 승인 루프 세팅.
> 내일 weekly에서 30분 dive.
>
> **Connor**: 정확히 필요하던 거야. Thanks.

**(이시현)** "시트 수기로 훑던 거, 대시보드로 한 번에 보니까 내일부터 바로 쓸 수 있어요."
**(백폴)** "P0별 원인이 다르다는 걸 데이터로 찍어본 건 처음이에요. 이제 Red 3개에 서로 다른 action이 붙어요."
**(황정기)** "샌프란 피드백 늦다는 느낌은 있었는데, 숫자로 보니까 확실해요."
**(Finance)** "TW billing이 Taiwan entity 세팅 때문이라는 걸 처음 봤어요."

---

## 데이터 파일

| 파일 | 내용 | 규모 |
|------|------|------|
| `speak_positions_master.csv` | 오픈 포지션 (priority, HM, target) | 12 |
| `speak_recruiting_pipeline_2601_2604.csv` | 후보자 (stage, ball_side, 방치일) | 222 |
| `speak_interview_feedback_2601_2604.csv` | 인터뷰 × 피드백 (인터뷰어 위치, 소요일) | 480 |
| `speak_contractor_lifecycle.csv` | Contractor (국가, stage, end_date) | 37 |
| `speak_finance_billing_issues_2601_2604.csv` | Billing 이슈 (contractor_id_link) | 175 |

**연결 키**: `position_id`, `candidate_id`, `contractor_id`
