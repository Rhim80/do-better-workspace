---
name: concept-fit
description: 본인 객단가·콘셉트가 후보지 상권에 적합한가 점수화. Concept Layer (Layer 3) 산출. entry-verdict의 보조 스킬. "concept-fit 한남", "객단가 맞나", "콘셉트 적합" 등 언급 시 자동 실행.
---

# concept-fit — 객단가·콘셉트 적합도 (내 가격대 맞는 동네인가?)

> **한 줄**: "내 객단가·콘셉트가 그 동네에 맞나?" — 상권 평균 대비 P30~P75 적정 구간 + 동일 콘셉트 점포 수.
> **언제 씀**: `entry-verdict`가 자동으로 부르는 보조 스킬. 단독 실행도 가능.
> **출력**: `50-resources/data/concept-fit-{zone}-{YYYYMMDD}.json` + 짧은 해석

---

## 사장님 입장에서 보면

**이게 뭘 해주나요?**
우리 객단가·콘셉트가 그 동네에 맞는지를 점수로 보여줍니다. 너무 비싸도 너무 싸도 안 맞음.

**이럴 때 쓰세요**
- "객단가 15,000원인데 이 동네에 맞나?"
- "스페셜티 카페 컨셉인데 비슷한 데 몇 개 있나?"
- "프리미엄 한식인데 이 동네 평균 객단가가 어떻게 되나?"

**결과로 손에 쥐는 것**
- **Concept 점수** (0-10): 객단가 위치 + 동일 콘셉트 점포 수 + 카테고리 매출 매칭
- **본인 객단가 percentile** (P30~P75가 자연스러운 구간)
- **동일 콘셉트 점포 수** (5개 미만 = 차별화 여지, 10개 초과 = 포화)
- 짧은 해석 + 경고

**주의**
- 객단가 P75 초과 = "비싸도 좋다" 아니라 회전율 부족 위험.
- 객단가 P30 미만 = 상권 평균보다 너무 저가, 손님이 안 찾을 위험.
- 콘셉트 카운트는 키워드 매칭 한계. 현장 답사로 보완 필수.

---

## 입력

- `personal-context.md` (본인 카테고리·객단가·콘셉트 키워드)
- 후보지 zone 이름

## 선행 조건

- `50-resources/data/zone-cache/{zone_name}.json` 존재

## 프로세스 (Concept Layer)

### Step 1 — 본인 객단가 percentile

```python
my_avg = personal_context.평균_객단가
zone_avg = zone_cache.spending.by_category[my_cat].avg_check_est
my_p_in_zone = percentile_rank(my_avg, zone_distribution[my_cat])
# P30 미만 또는 P75 초과면 미충족
```

### Step 2 — 동일 콘셉트 점포 카운트

콘셉트 키워드(예: "스페셜티 카페", "생면 파스타")로 매장명·메뉴 키워드 매칭.

부트캠프 시점은 mock 처리 — 진행자가 검색 결과 기반 입력 또는 zone-cache의 stores_by_category 활용.

```python
concept_count = zone_cache.supply.concept_count.get(my_concept, "추정")
# 5개 미만 충족, 5-10개 보류, 10개 초과 미충족
```

### Step 3 — 카테고리 매출 매칭

```python
category_p = zone_cache.spending.by_category[my_cat].p_seoul
# P50+ 충족, P30-50 보류, P30 미만 미충족
```

### Step 4 — Concept Score

```python
concept_score = (
    (10 if 30 <= my_p_in_zone <= 75 else 5) * 0.4 +
    (10 if concept_count < 5 else 5 if concept_count < 10 else 2) * 0.3 +
    (category_p / 100 * 10) * 0.3
)
```

## 출력

```json
{
  "zone": "한남동",
  "concept_score": 8.0,
  "components": {
    "my_avg_check": 9500,
    "zone_avg_check": 11500,
    "my_p_in_zone": 58,
    "concept_count_estimate": 4,
    "category_p_seoul": 71
  },
  "interpretation": "객단가 P58 — 상권 평균 대비 자연스러운 위치. 동일 콘셉트(스페셜티 카페) 4개로 차별화 여지. 카페 카테고리 P71 매출 수요 양호.",
  "warnings": []
}
```

## 체크리스트

- 본인 콘셉트 키워드 personal-context에 명시?
- 객단가 분포 데이터 zone-cache에 있나?
- 동일 콘셉트 점포 수 mock인가 실데이터인가 라벨?

## 주의

- 객단가 P75 초과 = 너무 비싸서 회전율 부족 위험. 단순 "비싸도 좋다" X.
- 객단가 P30 미만 = 상권 평균보다 너무 저가, 상권 손님이 안 찾을 위험.
- 콘셉트 카운트는 키워드 매칭 한계. 현장 답사 보완 필수.

## 참고

- entry-verdict (Layer 3 Concept 점수 입력)
- standard-fnb-personas.csv (페르소나-객단가 매핑 보조)
