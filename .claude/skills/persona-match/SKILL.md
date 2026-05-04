---
name: persona-match
description: 본인 페르소나(personal-context.md) ↔ 후보지 거주·생활인구 시간대 매칭. Volume + Rhythm Layer 점수 산출. entry-verdict의 보조 스킬. "persona-match 한남", "페르소나 맞나" 등 언급 시 자동 실행.
---

# persona-match — 내 손님 결 맞춤 (그 동네에 내 손님 있나?)

> **한 줄**: "내 손님이 그 동네에 충분히 있나, 우리 영업시간대에?" — 페르소나 비중 + 시간대 매칭을 0-10점으로.
> **언제 씀**: `entry-verdict`가 자동으로 부르는 보조 스킬. 단독 실행도 가능.
> **출력**: `50-resources/data/persona-match-{zone}-{YYYYMMDD}.json` + 짧은 해석

---

## 사장님 입장에서 보면

**이게 뭘 해주나요?**
우리 손님이 그 동네에 충분히 있는지, 그리고 우리 영업시간에 그 동네에 사람이 있는지를 점수로 보여줍니다.

**이럴 때 쓰세요**
- "20-30대 직장인 페르소나인데 거기 직장인 많나?"
- "심야 영업인데 그 동네 밤 인구 있나?"
- "주말 위주인데 주말 유동 어떤가?"

**결과로 손에 쥐는 것**
- **Volume 점수** (0-10): 거주민 + 유동인구 percentile
- **Rhythm 점수** (0-10): 우리 영업시간에 동네에 사람 있는 비율
- **매칭된 표준 페르소나** (P01~P07 중 가장 가까운 1-2개)
- 짧은 해석 + 경고 (예: "야간 21시 이후 빠짐")

**주의**
- 인구 통계 기반 추정. 실제 손님 결은 메뉴·마케팅 영향이 더 큼.
- 시간대 매칭이 낮아도 시그니처 메뉴·예약·플랫폼으로 보완 가능.

---

## 입력

- `personal-context.md` (페르소나 + 운영시간 + 객단가)
- 후보지 zone 이름 또는 좌표
- (선택) `50-resources/data/personas/standard-fnb-personas.csv` 표준 페르소나 매핑

## 선행 조건

- `50-resources/data/zone-cache/{zone_name}.json` 존재

## 프로세스

### Step 1 — 페르소나 표준화

`personal-context.md`의 페르소나를 `standard-fnb-personas.csv`의 P01~P07로 매핑:
- 비중 + 객단가 + 시간대 비교
- 가장 가까운 표준 페르소나 1-2개 선택

### Step 2 — Volume 매칭 (Layer 1)

```python
volume_score = (
    zone_cache.demand_volume.residents.p_seoul * 0.4 +
    zone_cache.demand_volume.floating.p_seoul * 0.6
) / 10  # 0-10 환산
```

페르소나 연령·성별 비중이 zone의 거주·생활인구 분포와 매칭되는 비율로 가중.

### Step 3 — Rhythm 매칭 (Layer 1.5)

```python
my_hours = personal_context.운영시간  # 예: 11:00~22:00
zone_hours = zone_cache.demand_rhythm.by_hour
match_ratio = sum(zone_hours[h] for h in my_active_hours)
rhythm_score = match_ratio * 10  # 0-10 환산
```

요일 매칭도 동일하게.

### Step 4 — 출력

```json
{
  "zone": "한남동",
  "matched_persona": ["P03 데이트·친구모임", "P05 가족·외식"],
  "volume_score": 7.1,
  "rhythm_score": 5.4,
  "interpretation": "거주민(P50) + 평일 직장인 유동(P88) 매칭. 운영시간대 매칭 52%. 단 야간(21시 이후) 빠짐.",
  "warnings": ["페르소나 P03 비중 30%인데 zone의 20-30대 여성 비중 P42 — 약간 빠짐"]
}
```

## 체크리스트

- personal-context.md에 페르소나 비중·시간대 명시?
- zone-cache에 demand_rhythm.by_hour 데이터 있나?
- 매칭 결과 Volume·Rhythm 점수 entry-verdict로 전달?

## 주의

- 페르소나 매칭은 인구 통계 기반 추정. 실제 손님 결은 운영·메뉴·마케팅 영향 큼.
- 시간대 매칭이 낮아도 시그니처 메뉴·예약·플랫폼으로 보완 가능.

## 참고

- standard-fnb-personas.csv (7종 표준 페르소나)
- entry-verdict (Layer 1·1.5 점수 입력으로 사용)
