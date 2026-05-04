---
name: competitive-pressure
description: 경쟁 밀도·가맹 포화·폐업률·카니발 거리 종합으로 Pressure Layer 점수 산출. entry-verdict의 보조 스킬. "competitive-pressure 한남", "경쟁 분석", "압력 점수" 등 언급 시 자동 실행.
---

# competitive-pressure — 경쟁 압력 점수 (거기 얼마나 빡센가?)

> **한 줄**: "그 동네 경쟁 얼마나 빡세?" — 경쟁 밀도 + 가맹 포화 + 폐업률 + 카니발(우리 매장 잠식) 거리 4축, 0-10점.
> **언제 씀**: `entry-verdict`가 자동으로 부르는 보조 스킬. 단독 실행도 가능.
> **출력**: `50-resources/data/competitive-pressure-{zone}-{YYYYMMDD}.json` + 짧은 해석

---

## 사장님 입장에서 보면

**이게 뭘 해주나요?**
그 동네에서 우리 카테고리가 얼마나 빡센지를 점수로 보여줍니다. 이미 가게 많은가, 가맹 많은가, 폐업 많은가, 우리 본점이랑 너무 가까운가 4축.

**이럴 때 쓰세요**
- "이 동네 카페 이미 한가득인데 들어가도 되나?"
- "우리 본점이랑 카니발(잠식) 안 나나?"
- "여기 폐업률 높던데 위험한가?"
- "가맹점이 많은 동네인가, 개인 매장이 많은가?"

**결과로 손에 쥐는 것**
- **Pressure 점수** (0-10): **점수 높을수록 압력 낮음 = 진입 양호**
- 4축 분해: 경쟁 밀도 percentile / 가맹 비중 / 폐업률 percentile / 우리 본점 거리
- 짧은 해석 + 경고 (예: "폐업률 P78 — 7CQ 미충족 트리거")

**주의**
- 가맹 데이터는 부트캠프 시점 mock. 별도 승인 후 실데이터 가능.
- 폐업률만 단독 판정 X. 신규개업률·점포 절대값과 같이 봐야.
- 카니발 거리는 직선거리 기준. 실제 도보·차량 동선 다를 수 있음.

---

## 입력

- `personal-context.md` (본인 매장 위치·카테고리·콘셉트)
- 후보지 zone 이름

## 선행 조건

- `50-resources/data/zone-cache/{zone_name}.json` 존재

## 프로세스 (Pressure Layer)

### Step 1 — 경쟁 밀도

```python
my_cat = personal_context.카테고리
density_p = zone_cache.supply.stores_by_category[my_cat].percentile_seoul  # P98이면 매우 포화
```

### Step 2 — 가맹 포화 (mock 처리)

가맹사업거래 API는 별도 승인 필요로 부트캠프 시점 제외. 대신:
- `zone_cache.supply.franchise_ratio_mock`의 추정값 사용
- 또는 진행자 직접 입력 (현장 조사 보완)

```python
franchise_ratio = zone_cache.supply.franchise_ratio_mock.get(my_cat, 0.30)
# 0.40 초과면 가맹 포화 위험 신호
```

### Step 3 — 폐업률

```python
close_rate_p = zone_cache.supply.close_rate_p_seoul[my_cat]
# P75 초과면 미충족 (CQ4 트리거)
```

### Step 4 — 카니발 거리

```python
my_existing_stores = personal_context.기존_매장_좌표[]
distances = [haversine(zone.geo, store) for store in my_existing_stores]
min_dist_km = min(distances)
# 3km 미만이면 카니발 위험
```

### Step 5 — Pressure Score 합산

```python
pressure_score = 10 - (
    density_p / 100 * 4.0 +       # 경쟁 밀도 비중 40%
    franchise_ratio * 10 * 2.0 +  # 가맹 비중 20%
    close_rate_p / 100 * 3.0 +    # 폐업률 비중 30%
    (3.0 - min(min_dist_km, 3.0)) / 3.0 * 1.0  # 카니발 비중 10%
)
# 점수 높을수록 압력 낮음 (진입 양호)
```

## 출력

```json
{
  "zone": "한남동",
  "pressure_score": 6.2,
  "components": {
    "density_p": 78,
    "franchise_ratio": 0.42,
    "close_rate_p": 78,
    "cannibal_min_dist_km": 4.2
  },
  "interpretation": "카페 92개 P98 + 폐업률 P78 — 진입 시 차별화 필수. 가맹 비중 42%로 가맹 포화 신호. 본인 본점 4.2km로 카니발 안전.",
  "warnings": ["폐업률 P78 — CQ4 미충족 트리거"]
}
```

## 체크리스트

- 본인 기존 매장 좌표 personal-context에 있나?
- zone-cache에 supply.close_rate_p_seoul 있나?
- 가맹 데이터 mock 처리되어 있는가?

## 주의

- 가맹사업거래 API 별도 승인 시 정확한 가맹점 데이터 사용 가능. 부트캠프 시점은 mock.
- 폐업률 단독 판정 금지. 신규개업률·점포 절대값과 함께.
- 카니발 거리는 직선거리 기준. 실제 도보·차량 동선 다를 수 있음.

## 참고

- entry-verdict (Layer 2 Pressure 점수 입력)
- references는 entry-verdict의 magnitude-estimation.yaml 임계치 공유
