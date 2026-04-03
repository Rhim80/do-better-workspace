# 관광객 세그먼테이션 분석 프레임워크

> 기반: Market Segmentation (Smith, 1956), Cross-tabulation, Pareto Principle

---

## 1. 시장 세그먼테이션 (Market Segmentation)

**출처**: Wendell R. Smith (1956). "Product Differentiation and Market Segmentation as Alternative Marketing Strategies". Journal of Marketing
**발전**: Kotler & Keller (2016). Marketing Management, 15th Edition. Pearson

**핵심**: 이질적인 시장을 동질적인 하위 그룹으로 나누어 차별화된 전략 수립

### 세그먼테이션 기준 (STP 모델의 S)

| 기준 | 설명 | 뉴믹스 적용 |
|------|------|-------------|
| 지리적 (Geographic) | 국가, 지역 | 고객국적 컬럼 |
| 인구통계적 (Demographic) | 나이, 성별 | 데이터 없음 |
| 행동적 (Behavioral) | 구매 패턴, 선호 상품 | 상품명, 수량, 합계 |
| 심리적 (Psychographic) | 라이프스타일 | 데이터 없음 |

> 뉴믹스 데이터는 **지리적(국적) + 행동적(구매)** 세그먼테이션이 가능

### 관광 시장 세그먼테이션 특수성

**출처**: Dolnicar, S. (2008). "Market Segmentation in Tourism". In Tourism Management: Analysis, Behaviour and Strategy. CABI

관광 소비 분석에서의 핵심 변수:

```
1. 출발 국가 (Origin Market)
   → 국적별 구매력, 문화적 선호, 체류 기간 차이

2. 지출 패턴 (Expenditure Pattern)
   → 객단가, 구매 수량, 선호 카테고리

3. 시간 패턴 (Temporal Pattern)
   → 방문 시간대, 요일, 계절성
```

---

## 2. 교차분석 (Cross-tabulation)

**출처**: Karl Pearson (1900). 범주형 변수 간 관계 분석의 표준 통계 기법
**실무 도구**: Excel 피벗 테이블, pandas crosstab

**핵심**: 두 개 이상의 범주형 변수를 동시에 집계하여 패턴 발견

### 교차분석 매트릭스

```
              상품 A    상품 B    상품 C    합계
일본            120       45        30      195
대만             80       60        25      165
미국             40       30        55      125
한국             30       20        15       65
합계            270      155       125      550
```

### 분석 축 조합

| 교차 축 | 발견할 수 있는 것 |
|---------|------------------|
| 국적 x 상품 | 국가별 선호 상품 차이 |
| 국적 x 시간대 | 국가별 방문 시간 패턴 |
| 국적 x 카테고리 | 국가별 구매 카테고리 비중 |
| 국적 x 결제수단 | 국가별 결제 선호도 |

---

## 3. 핵심 지표 (KPI)

### 세그먼트별 필수 지표

| 지표 | 공식 | 의미 |
|------|------|------|
| 매출 비중 | 세그먼트 매출 / 전체 매출 x 100 | 해당 국적의 매출 기여도 |
| 객단가 (ATV) | 세그먼트 총매출 / 세그먼트 주문 수 | 1회 방문 평균 지출 |
| 구매 수량 (UPT) | 세그먼트 총수량 / 세그먼트 주문 수 | 1회 방문 평균 구매 개수 |
| 집중도 (HHI) | 각 세그먼트 비중^2의 합 | 특정 국적 의존도 |

> ATV = Average Transaction Value, UPT = Units Per Transaction
> 출처: Retail KPI 표준 (NRF - National Retail Federation)

### 집중도 해석 (Herfindahl-Hirschman Index)

**출처**: Herfindahl (1950), Hirschman (1964). 시장 집중도 측정 표준 지표

```
HHI = Σ(각 세그먼트 비중%)^2

해석:
- HHI < 1,500: 분산된 구조 (건강)
- 1,500 < HHI < 2,500: 중간 집중 (모니터링)
- HHI > 2,500: 높은 집중 (리스크)

예시:
- 일본 40%, 대만 25%, 미국 15%, 한국 10%, 기타 10%
- HHI = 40² + 25² + 15² + 10² + 10² = 1,600 + 625 + 225 + 100 + 100 = 2,650
- → 일본 의존도가 높음, 분산 필요
```

---

## 4. Pareto 분석 적용

**출처**: Vilfredo Pareto (1896). Cours d'economie politique

### 고객 세그먼트에 적용

```
1단계: 국적별 매출 내림차순 정렬
2단계: 누적 비중 계산
3단계: 상위 20% 국적이 전체 매출의 몇 %인지 확인

→ 상위 2~3개국이 80% 이상이면 전형적 파레토
→ 해당 국가에 마케팅/상품 전략 집중
```

---

## 5. 실습 적용 예시

### 프롬프트 템플릿

```
"[매출 데이터 파일]에서 고객 세그먼트별 분석해줘.

@tourism-segmentation-framework.md 관점으로:
- 세그먼트별 매출 비중과 Pareto 분석
- 세그먼트 x 상품 교차분석 (상위 5개 그룹, 인기 상품 TOP 3)
- 세그먼트별 객단가(ATV)와 구매수량(UPT) 비교
- 시간대별 방문 패턴 교차분석
- HHI로 특정 세그먼트 의존도 체크"
```

---

## 6. CEO 보고 시 핵심 메시지 구조

```markdown
## 인바운드 고객 분석

### 핵심 숫자
- 외국인 매출 비중: OO% (전월 대비 +OO%p)
- 1위 국적: OO (매출 OO%, 객단가 OO원)
- 국적 집중도(HHI): OO (높음/중간/분산)

### 국적별 선호 상품 (교차분석)
| 국적 | 1위 상품 | 2위 상품 | 객단가 |
|------|---------|---------|--------|
| | | | |

### So What
- [데이터가 말하는 핵심 인사이트]

### Now What
- [국적별 맞춤 전략 제안]
```

---

## 참고 자료

- Smith, W. (1956). Product Differentiation and Market Segmentation. Journal of Marketing
- Kotler, P. & Keller, K. (2016). Marketing Management, 15th Edition. Pearson
- Dolnicar, S. (2008). Market Segmentation in Tourism. CABI
- Herfindahl, O. (1950). Concentration in the Steel Industry. Columbia University
- NRF (National Retail Federation). Retail Metrics Standards
