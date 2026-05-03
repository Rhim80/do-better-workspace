---
name: entry-verdict
description: 신규 출점 후보지에 대한 의사결정 판정. 5-Layer 점수 + Magnitude(월매출 잠재력 ± · BEP 임대 vs 실제 시세) + Toulmin 6요소 + 7 Critical Questions 점검 → Go/Conditional/No-Go 판정. 한 페이지 리포트 출력. "entry-verdict 한남", "여기 들어갈까", "출점 판정", "이 상권 진입" 등 언급 시 자동 실행.
---

# entry-verdict — 신규 출점 의사결정 판정

> **역할**: "이 자리 들어갈까?"에 5-Layer 분석 + Toulmin 논증 + Magnitude 추정으로 답하는 WOW 핵심 스킬.
> **출력**: `data/verdict-{zone_name}-{YYYYMMDD}.md` + HTML 한 페이지 카드

---

## 입력

- `personal-context.md` (본인 매장·페르소나·객단가·운영시간·평수·임대비중 한도)
- 후보지 zone 이름 (행정동) — 또는 좌표
- 후보지 평수 (선택, 미입력 시 본인 매장 평수와 같다고 가정)

## 선행 조건

- `data/zone-cache/{zone_name}.json` 존재 (없으면 zone-fetch 자동 호출)
- 보조 스킬 결과 권장 (없어도 동작): `persona-match`, `competitive-pressure`, `concept-fit`

## 프로세스

### Step 1 — 5-Layer 점수 산출

| Layer | 산출 | 0-10점 |
|-------|------|--------|
| Volume | 거주+생활인구 percentile 평균 | persona-match 호출 결과 또는 자체 계산 |
| Rhythm | 운영시간대 ↔ 시간대 생활인구 매칭 비율 | persona-match |
| Pressure | 경쟁 밀도 + 가맹 포화 + 폐업률 + 카니발 거리 종합 | competitive-pressure |
| Concept | 상권 평균 객단가 ↔ 본인 객단가 + 동일 컨셉 점포 카운트 | concept-fit |
| (Verdict는 종합) | — | — |

### Step 2 — Magnitude 추정 (★ WOW 핵심)

```python
# 1. 후보지 평당 매출 추정 (P25/P50/P75)
sales_per_pyeong = {
    "p25": zone_cache.spending.by_category[my_cat].monthly_per_pyeong * 0.75,
    "p50": zone_cache.spending.by_category[my_cat].monthly_per_pyeong,
    "p75": zone_cache.spending.by_category[my_cat].monthly_per_pyeong * 1.30,
}

# 2. 월매출 시나리오
candidate_pyeong = personal_context.candidate_size or personal_context.size
monthly_revenue = {
    "보수": sales_per_pyeong.p25 * candidate_pyeong,
    "중립": sales_per_pyeong.p50 * candidate_pyeong,
    "낙관": sales_per_pyeong.p75 * candidate_pyeong,
}

# 3. BEP 임대 (월매출 × 임대비중 한도)
rent_ratio_max = personal_context.rent_ratio_max or 0.10  # references/magnitude-estimation.yaml
bep_rent = monthly_revenue.중립 * rent_ratio_max

# 4. 실제 시세 비교
actual_rent = (
    zone_cache.real_estate.naver_p50_monthly_per_pyeong * candidate_pyeong
    if zone_cache.real_estate.naver_listings else
    zone_cache.real_estate.rone_p50_per_pyeong_monthly * candidate_pyeong
)

# 5. Δ% 계산
delta_pct = (actual_rent - bep_rent) / bep_rent * 100
```

### Step 3 — Toulmin 6요소 분해

`references/walton-cq-fnb.md`의 템플릿 사용:

```
Claim:    "{zone}는 {brand}에 [Go/Conditional/No-Go]"
Grounds:  Layer 1-3 점수 + Magnitude 결과 인용 (각 데이터 출처 명시)
Warrant:  "Volume·Rhythm·Spending이 P50+ 이고 폐업률 P75 미만이면 진입 가능하다"
          (조건부 일반화 — 산업 통계 기반)
Backing:  외식업 신규점 1년 생존율 등 산업 통계 (references)
Qualifier: 어떤 조건에서만 유효 (예: "낙관 시나리오 P75 평당매출 달성 시")
Rebuttal: 어떤 조건에서 무효 (예: "임대 시세가 BEP 25% 초과 시 무효")
```

### Step 4 — 7 Critical Questions 점검

각 질문에 충족(✅) / 미충족(❌) / 판단보류(⚠️) + 근거 1-2문장:

1. **Volume**: 페르소나 살고/머무는가? — Layer 1 점수 P50+면 충족
2. **Rhythm**: 운영시간대 매칭? — Layer 1.5 매칭 ≥40%면 충족
3. **Spending**: 업종에 돈 쓰는가? — 추정매출 P50+면 충족
4. **Saturation**: 카테고리 작동? 틈 있나? — 폐업률 P75 미만 + 동일 컨셉 점포 < 5개면 충족
5. **Cannibal**: 본인 매장 영향? — 거리 ≥3km 또는 영업시간 분리 시 충족
6. **Concept**: 객단가·컨셉 일관성? — 본인 객단가가 상권 P30~P75 범위 내면 충족
7. **Magnitude**: 임대 정당화? — Δ% ≤ 10% 충족, 10~30% 보류, >30% 미충족

각 임계치는 `references/magnitude-estimation.yaml`에서 수정 가능.

### Step 5 — Verdict 판정

```
충족 ≥ 5 + 미충족 ≤ 1 → Go
충족 4 + 미충족 2-3 → Conditional (조건 명시)
미충족 ≥ 4 또는 Magnitude 미충족 → No-Go
```

Conditional 시 **재검토 조건** 자동 도출 (예: "임대 1,400만 이하 협상", "70평+ 확장").

### Step 6 — 현장 답사 체크리스트 3-5개

미충족·보류 CQ에서 도출:
- "심야 21시 유동인구 직접 확인"
- "동일 컨셉 6개 점포 메뉴 가격대 확인"
- "전면 가시성 / 도보 동선"
- "지하 vs 지상 임대 시세 차이"
- "주말 vs 평일 손님 결 차이"

### Step 7 — 한 페이지 카드 출력

`references/entry-verdict-template.md` 사용. zone-report 호출 → HTML/PDF.

```
┌─────────────────────────────────────────────────┐
│ [Verdict: Conditional] · 한남동 50평 · 이미커피 2호│
├─────────────────────────────────────────────────┤
│ Magnitude (월매출 잠재력)                        │
│   보수 0.42억 · 중립 0.55억 · 낙관 0.71억        │
│   BEP 임대 550만 │ 시세 720만 │ Δ +31%           │
├─────────────────────────────────────────────────┤
│ 5-Layer Score                                   │
│   Volume   ███████░░░ 7.1                       │
│   Rhythm   █████░░░░░ 5.4                       │
│   Pressure ▓▓▓▓▓▓▒▒▒▒ 6.2 (폐업률 P78 경고)     │
│   Concept  ████████░░ 8.0                       │
├─────────────────────────────────────────────────┤
│ 7 CQ:  ✅✅⚠️❌✅✅❌  (4 / 2 / 1)               │
├─────────────────────────────────────────────────┤
│ Toulmin: "수요·컨셉 적합, 그러나 폐업률+임대가    │
│ 동시에 부담 — 임대 협상 또는 평수 확장 시 재검토" │
├─────────────────────────────────────────────────┤
│ 재검토 조건: 임대 600만 이하 / 70평+ 확장        │
│ 현장 답사 5개 체크리스트                          │
└─────────────────────────────────────────────────┘
```

## 비교 매트릭스 (3개 후보 동시 호출 시)

```bash
entry-verdict 한남동
entry-verdict 성수동
entry-verdict 압구정동
```

→ 자동으로 비교 매트릭스 생성 (`data/verdict-comparison-{YYYYMMDD}.md`):
- 5-Layer 점수 나란히 비교
- Magnitude 비교 표
- 7 CQ 매트릭스
- 추천 후보 + 핵심 리스크

## 체크리스트

- `personal-context.md`에 페르소나·객단가·운영시간·평수·rent_ratio_max 명시?
- zone-cache에 spending.by_category 데이터 있는가? (없으면 Magnitude 추정 불가)
- `references/magnitude-estimation.yaml` 임계치 적정한가? (필요 시 사용자 조정 가이드)

## 주의

- Magnitude는 **모델링 추정치**. "실제 매출은 운영 역량·마케팅·메뉴 영향 큼" 라벨 필수
- BEP 임대는 의사결정 가이드. 실제 시세는 부동산 플랫폼 호가로 검증
- Verdict는 **자리 결정자가 아니라 의사결정 보조 도구**. 최종 판단은 사람
- 7 CQ 임계치(P50, P75 등)는 기본값. 본인 사업 특성에 맞춰 조정 필수

## 참고

- references/walton-cq-fnb.md (Toulmin 6요소 + 7 CQ + Walton 도식)
- references/magnitude-estimation.yaml (임계치·계수 수정 가능)
- references/entry-verdict-template.md (한 페이지 카드)
- references/bias-traps-fnb.md (외식업 의사결정 흔한 편향)
