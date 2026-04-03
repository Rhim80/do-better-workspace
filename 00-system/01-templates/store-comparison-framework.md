# 매장 비교 분석 프레임워크

> 기반: Benchmarking (Camp, 1989), Comp Store Sales, Retail KPI Standards

---

## 1. 벤치마킹 (Benchmarking)

**출처**: Robert C. Camp (1989). Benchmarking: The Search for Industry Best Practices. ASQC Quality Press
**발전**: Xerox Corporation이 1979년 최초 체계화, 이후 경영학 표준 기법으로 정착

**핵심**: 동일 기준으로 대상을 비교하여 차이의 원인을 분석하고 개선 방향 도출

### 벤치마킹 유형

| 유형 | 비교 대상 | 뉴믹스 적용 |
|------|----------|-------------|
| 내부 벤치마킹 (Internal) | 같은 조직 내 다른 부서/매장 | 성수점 vs 북촌점 |
| 경쟁 벤치마킹 (Competitive) | 동종 경쟁사 | 타 F&B 브랜드 (데이터 없음) |
| 기능 벤치마킹 (Functional) | 이종 산업 우수 사례 | 해당 없음 |

> 뉴믹스 데이터는 **내부 벤치마킹** - 동일 브랜드 내 매장 비교

---

## 2. 동일 매장 매출 비교 (Comp Store Sales)

**출처**: 미국 소매업 표준 지표. SEC(미국 증권거래위원회) 공시 기준
**활용**: Starbucks, McDonald's 등 글로벌 체인이 분기 실적 발표 시 핵심 지표로 사용

**핵심**: 동일 조건(기간, 영업일수)에서 매장 간 성과를 비교

### 비교 전 정규화

```
동일 기간 비교가 기본:
- 같은 달(2월), 같은 영업일수 확인
- 매장 규모(평수) 차이가 크면 면적당 매출(Sales per sqft)로 보정
- 오픈 시기 차이 고려 (성수 2024.3 vs 북촌 2025.3)
```

> 성수점이 1년 먼저 오픈 → 인지도/단골 차이 감안 필요

---

## 3. 소매 핵심 성과 지표 (Retail KPIs)

**출처**: NRF (National Retail Federation) Retail Metrics Standards
**보충**: Levy, M. & Weitz, B. (2012). Retailing Management, 8th Edition. McGraw-Hill

### 매장 비교 필수 KPI 5개

| KPI | 공식 | 의미 |
|-----|------|------|
| 총매출 (Revenue) | SUM(합계) | 절대적 규모 |
| 주문 수 (Transactions) | COUNT(DISTINCT 주문번호) | 구매 고객 수 |
| 객단가 (ATV) | 총매출 / 주문 수 | 1회 방문 지출 |
| 구매수량 (UPT) | 총수량 / 주문 수 | 1회 방문 구매 개수 |
| 카테고리 믹스 | 카테고리별 매출 비중 | 매장 성격 차이 |

### 보조 KPI

| KPI | 공식 | 의미 |
|-----|------|------|
| 외국인 비중 | 외국인 매출 / 총매출 x 100 | 인바운드 의존도 |
| 국적 구성 | 국적별 비중 | 타깃 고객 차이 |
| 시간대 분포 | 시간대별 주문 수 | 피크 타임 차이 |
| 결제수단 비중 | 결제수단별 비율 | 고객 유형 |

---

## 4. 비교 분석 매트릭스

### 갭 분석 (Gap Analysis)

**출처**: 전략 경영 표준 기법. Parasuraman, A. et al. (1985). SERVQUAL

```
갭 = 매장 A 지표 - 매장 B 지표

해석:
- 양수: A가 우위
- 음수: B가 우위
- 갭 크기: 차이의 유의미성 판단
```

### 비교 매트릭스 구조

```
                    성수점      북촌점      갭(차이)     해석
총매출              OO만원      OO만원      +OO만원     성수 우위
주문 수             OO건        OO건        +OO건
객단가(ATV)         OO원        OO원        -OO원       북촌 우위
외국인 비중         OO%         OO%         +OO%p
1위 국적            OO          OO                      타깃 차이
1위 상품            OO          OO                      선호 차이
```

---

## 5. 포트폴리오 관점: 매장 역할 분류

**출처**: BCG Growth-Share Matrix (Henderson, 1970) 응용

### 매장 포지셔닝

```
                    매출 규모
                 큼              작음
         ┌────────────────┬────────────────┐
    높   │   Flagship     │   Incubator    │
 성 음   │  (수익 창출)    │  (테스트 매장)  │
 장      ├────────────────┼────────────────┤
 률 낮   │   Steady       │   Watch        │
    음   │  (안정 수익)    │  (개선 필요)    │
         └────────────────┴────────────────┘
```

> 성수점: 1년차 Flagship 가능성, 북촌점: 1년 미만 Incubator 단계

---

## 6. 상품 믹스 비교

### 상품 포지셔닝 매트릭스

```
같은 상품이 매장별로 다른 포지션:

                    성수 순위
                 상위           하위
         ┌────────────────┬────────────────┐
    상   │   공통 히트     │   북촌 강세    │
 북 위   │ (양쪽 모두 인기)│ (북촌 특화 수요)│
 촌      ├────────────────┼────────────────┤
 순 하   │   성수 강세     │   저성과       │
 위 위   │ (성수 특화 수요)│ (양쪽 모두 부진)│
         └────────────────┴────────────────┘
```

### 한정 상품 성과 평가

```
한정 상품 기여도 = 한정 상품 매출 / 해당 매장 총매출 x 100

해석:
- 5% 이상: 유의미한 기여 → 유지/확대
- 1~5%: 보통 → 프로모션으로 인지도 강화
- 1% 미만: 미미 → 대체 상품 검토
```

---

## 7. 실습 적용 예시

### 프롬프트 템플릿

```
"[매장 A 매출 파일]과 [매장 B 매출 파일]을 비교 분석해줘.

@store-comparison-framework.md 관점으로:
- 5대 KPI 비교 (매출, 주문 수, 객단가, 구매수량, 카테고리 믹스)
- 고객 구성 차이 (외국인 비중, 국적, 연령대 등)
- 공통 히트 상품 vs 매장별 강세 상품 구분
- 매장 한정 상품의 매출 기여도
- 두 매장의 포지셔닝 차이에 따른 전략 제안"
```

---

## 8. CEO 보고 시 핵심 메시지 구조

```markdown
## 매장 비교 분석 (성수 vs 북촌)

### 핵심 숫자
| 지표 | 성수 | 북촌 | 갭 |
|------|------|------|-----|
| 총매출 | | | |
| 객단가 | | | |
| 외국인 비중 | | | |

### 매장 포지셔닝
- 성수: [Flagship/Steady] - [특성 설명]
- 북촌: [Incubator/Watch] - [특성 설명]

### So What
- [두 매장의 핵심 차이점]

### Now What
- [매장별 차별화 전략 또는 통일 전략 제안]
```

---

## 참고 자료

- Camp, R. (1989). Benchmarking: The Search for Industry Best Practices. ASQC Quality Press
- Levy, M. & Weitz, B. (2012). Retailing Management, 8th Edition. McGraw-Hill
- Henderson, B. (1970). The Product Portfolio. BCG Perspectives
- NRF (National Retail Federation). Retail Metrics Standards
- Parasuraman, A., Zeithaml, V. & Berry, L. (1985). A Conceptual Model of Service Quality. Journal of Marketing
