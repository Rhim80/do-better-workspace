---
name: zone-fetch
description: 행정동 또는 좌표 입력 시 12개 데이터 소스(공공 API 9 + Google Trends + 통계청 SGIS + 네이버 부동산 크롤링)를 병렬 호출하여 표준화된 zone-cache JSON을 생성. zone-diagnosis와 entry-verdict의 데이터 엔진. "zone-fetch 한남동", "한남 데이터 가져와", "이 좌표 상권 데이터" 등 언급 시 자동 실행.
---

# zone-fetch — 상권 데이터 모으기 (12개 소스 한 번에)

> **한 줄**: "이 동네 데이터 다 가져와" — 행정동/좌표만 주면 12개 공공 데이터 소스에서 한 번에 수집.
> **이 스킬은 보통 `zone-diagnosis`·`entry-verdict`가 필요할 때 자동으로 먼저 돌아갑니다. 직접 부를 일은 거의 없음.**
> **출력**: `50-resources/data/zone-cache/{행정동명}.json`

---

## 사장님 입장에서 보면

**이게 뭘 해주나요?**
우리 동네(또는 후보 동네) 데이터를 12군데서 한 번에 모아옵니다. 인구·매출·임대·외국인·검색까지 한 번에. 매번 받으면 30~60초 걸리니까 한 번 받아두면 캐시에 넣어두고 다음부턴 즉시 봅니다.

**이럴 때 쓰세요**
직접 부를 일은 거의 없어요. **`zone-diagnosis`(내 자리 진단)**나 **`entry-verdict`(새 자리 판정)**를 부르면 자동으로 먼저 돌아갑니다. 데이터가 너무 오래된 것 같으면 그때 직접 한 번 다시 돌리는 정도.

**결과로 손에 쥐는 것**
동 단위 raw 데이터 묶음 (JSON 파일). 사람이 직접 읽기엔 너무 큼 — 진단·판정 스킬이 이걸 해석해서 한 페이지 카드로 뽑아줍니다.

**주의**
- 라이브 호출은 30~60초 대기. 시연·실시간 보여주기엔 사전 캐시 권장.
- 부분 실패 허용 — 12개 중 1-2개 빠져도 나머지로 진단·판정 가능.

---

## 입력 형태

다음 중 하나:
- 행정동 이름 (예: "한남동", "홍대입구")
- 행정동 코드 (예: "11170102")
- 위경도 좌표 + 반경 (예: `37.520,127.023 r=500`)
- 주소 (자동 지오코딩)

## 호출 10개 소스 (2026-05-04 기준 작동 상태)

| # | 데이터 | 모듈 | 작동 |
|---|--------|------|------|
| 1 | 행안부 통반단위 주민등록 인구 | `modules/public_api.py::fetch_population` | ✅ |
| 2 | 소진공 상가(상권)정보 | `modules/public_api.py::fetch_stores` | ✅ |
| 3 | 국토부 상업업무용 매매 실거래 | `modules/public_api.py::fetch_realestate_offi` | ❌ endpoint 미확인 |
| 4 | 한국문화관광연구원 외래관광객 | `modules/public_api.py::fetch_foreign_visit` | ❌ endpoint 미확인 |
| 5 | KT 생활인구 (행정동 분기) | `modules/seoul_api.py::fetch_living_pop` | ✅ |
| 6 | 우리마을가게 추정매출 (분기) | `modules/seoul_api.py::fetch_sales_estimate` | ✅ |
| 7 | 우리마을가게 상권변화지표 | `modules/seoul_api.py::fetch_zone_change` | ✅ |
| 8 | 한국부동산원 R-One 상가 임대료 | `modules/rone_api.py::fetch_rone_rent` | ✅ |
| 9 | KOSIS 인구·통계 | `modules/kosis_api.py::fetch_population_kosis` | ✅ |
| 10 | Google Trends | `modules/pytrends_module.py::fetch_search_interest` | ✅ |
| - | 공정위 가맹점수 | (제외 — 별도 승인 필요) | - |

## 실행

```bash
cd .claude/skills/zone-fetch
python3 -m modules.orchestrator 한남동
# → /50-resources/data/zone-cache/한남동.live.json 생성 (raw 데이터)
```

지원 zone: `홍대입구, 한남동, 성수동, 압구정동` (zone_codes.py에 매핑). 새 zone 추가 시 zone_codes.py에 행정동·상권 코드 등록.

## 의존성

`pip3 install -r requirements.txt`
- httpx (병렬 HTTP)
- pytrends (Google Trends)

### 추가 데이터 3종

| # | 데이터 | 모듈 | 비고 |
|---|--------|------|------|
| 10 | Google Trends (지역+업종 검색 추세) | `modules/pytrends_module.py` | 무료, 키 불필요 |
| 11 | 통계청 SGIS (사업체·종사자·소득) | `modules/public_api.py::fetch_sgis` | 선택 |
| 12 | 네이버 부동산 매물 (상가 호가) | `modules/naver_rent.py` | 비공식 API, Header 위장 + Rate limit 5초 sleep |

## 출력 JSON 스키마

`50-resources/data/zone-cache/{zone_name}.json`:

```json
{
  "zone_id": "11170102",
  "zone_name": "한남동",
  "geo": {"lat": 37.535, "lng": 127.001, "radius_m": 500},
  "fetched_at": "2026-05-03T14:30:00",
  "sources": {
    "행안부": {"period": "2025-12", "ok": true},
    "KT생활인구": {"period": "2025-Q4", "ok": true},
    "추정매출": {"period": "2025-Q4", "ok": true},
    "소진공": {"period": "2025-12", "ok": true},
    "공정위": {"period": "2024", "ok": true},
    "상권변화": {"period": "2025-Q4", "ok": true},
    "실거래": {"period": "2025-Q4", "ok": true},
    "R-One임대": {"period": "2025-Q4", "ok": true},
    "관광공사외국인": {"period": "2025-Q4", "ok": true},
    "GoogleTrends": {"period": "2024-11~2025-12", "ok": true},
    "네이버부동산": {"period": "2026-05-03 호가", "ok": true, "count": 12}
  },
  "demand_volume": {
    "residents": {"total": 12500, "by_age_gender": {...}},
    "floating": {"avg_daily": 45200, "p_seoul": 78}
  },
  "demand_rhythm": {
    "by_hour": {"09": 0.10, "12": 0.18, "15": 0.16, "18": 0.22, "21": 0.18, "00": 0.08},
    "by_day": {"mon": 0.13, "tue": 0.14, "wed": 0.14, "thu": 0.15, "fri": 0.16, "sat": 0.15, "sun": 0.13}
  },
  "demand_timeseries": {
    "quarters": ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"],
    "living_pop": [44200, 44800, 45100, 45500, 45200, 45800, 45200, 45200],
    "sales_total": [105e8, 102e8, 99e8, 95e8, 92e8, 90e8, 87e8, 85e8],
    "foreign_visit": [820, 950, 1020, 980, 760, 680, 580, 520]
  },
  "spending": {
    "by_category": {
      "한식": {"quarterly_total": 8500000000, "p_seoul": 65, "avg_check_est": 24000},
      "카페": {"quarterly_total": 4200000000, "p_seoul": 88, "avg_check_est": 8500},
      "양식": {...}
    }
  },
  "supply": {
    "stores_by_category": {"한식": 38, "카페": 92, "한식·구이": 4},
    "franchise_ratio": {"한식": 0.18, "카페": 0.42},
    "open_close_4q": {"한식": {"new": 5, "closed": 8}, "카페": {"new": 12, "closed": 14}}
  },
  "real_estate": {
    "rone_p50_per_pyeong_monthly": 280000,
    "rone_p50_deposit_per_pyeong": 5000000,
    "naver_listings": [
      {"size_pyeong": 25, "deposit": 100000000, "monthly": 7500000, "floor": "1F", "url": "..."},
      ...
    ],
    "naver_p50_monthly_per_pyeong": 320000
  },
  "search_interest": {
    "keyword": "한남동 카페",
    "monthly": [{"month": "2024-11", "value": 65}, ...]
  }
}
```

## 프로세스

1. **입력 정규화** — 행정동 코드로 변환 (지오코딩 또는 lookup table)
2. **캐시 확인** — `50-resources/data/zone-cache/{zone_name}.json` 존재 + 7일 이내면 그대로 반환
3. **병렬 호출** — 12개 소스를 asyncio로 병렬 호출 (호출당 timeout 10초)
4. **부분 실패 허용** — 1-2개 실패해도 나머지로 JSON 생성. `sources[X].ok=false` 명시
5. **표준화** — 각 소스 응답을 위 스키마로 매핑
6. **저장** — `50-resources/data/zone-cache/{zone_name}.json` write

## 체크리스트

- `.env.local`에 5종 키 채워졌는가?
- pytrends 설치됐는가? (`pip install pytrends`)
- 네이버 크롤링 모듈의 Header 위장이 활성인가?
- 캐시 폴더 쓰기 권한 있는가?

## 주의

- 네이버 부동산 호출은 5초 sleep 필수. 하루 200회 이내로 제한.
- 공공 API rate limit 1,000/일은 1개 zone-fetch에 약 9 호출 → 일 100 zone 정도.
- 부분 실패 시 entry-verdict는 작동하나 정확도 한정 → 리포트 푸터에 "데이터 미수집" 라벨 명시.

## 참고

- references는 별도 없음. 모듈 코드 자체가 reference.
- 네이버 크롤링 패턴: https://github.com/ByungJin-Lee/NaverRealEstateHavester
