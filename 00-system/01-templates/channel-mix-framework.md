# 채널 믹스 분석 프레임워크

> 기반: Marketing Mix - Place (McCarthy, 1960), Channel Contribution Analysis, Geographic Demand Mapping

---

## 1. 채널 전략 기초: 마케팅 믹스의 Place

**출처**: E. Jerome McCarthy (1960). Basic Marketing: A Managerial Approach. Richard D. Irwin
**발전**: Kotler & Keller (2016). Marketing Management. Chapter 17: Designing and Managing Integrated Marketing Channels

**핵심**: 마케팅 4P(Product, Price, Place, Promotion) 중 Place = 유통 채널 전략

### 채널 유형

| 유형 | 특성 | 뉴믹스 적용 |
|------|------|-------------|
| 직접 채널 (Direct) | 자사 매장/사이트 | 성수점, 북촌점, 자사몰 |
| 간접 채널 (Indirect) | 유통 플랫폼 경유 | 네이버, 쿠팡, 컬리 |
| 옴니채널 (Omnichannel) | 온오프 통합 | 전채널 합산 분석 |

---

## 2. 채널 기여도 분석 (Channel Contribution Analysis)

**출처**: Neslin, S. et al. (2006). "Challenges and Opportunities in Multichannel Customer Management". Journal of Service Research

**핵심**: 각 채널이 전체 매출에 기여하는 비중과 효율성을 측정

### 채널별 핵심 KPI

| KPI | 공식 | 의미 |
|-----|------|------|
| 매출 비중 | 채널 매출 / 전체 온라인 매출 x 100 | 채널의 매출 기여도 |
| 주문 수 | COUNT(DISTINCT 주문번호) | 채널별 거래 규모 |
| 객단가 (ATV) | 채널 매출 / 채널 주문 수 | 채널별 구매 규모 |
| 주문 완료율 | 배송완료 수 / 전체 주문 수 x 100 | 채널 품질 |
| 취소율 | 취소 수 / 전체 주문 수 x 100 | 채널 리스크 |

### 채널 집중도 (HHI)

**출처**: Herfindahl (1950), Hirschman (1964)

```
HHI = Σ(각 채널 매출 비중%)^2

해석:
- 한 채널이 80% 이상: 과도한 의존 → 채널 다각화 필요
- 3개 채널이 균등 (33%씩): HHI ≈ 3,333 → 적정 분산
- 5개 채널이 균등 (20%씩): HHI = 2,000 → 잘 분산

예시:
- 컬리 55%, 네이버 30%, 쿠팡 15%
- HHI = 55² + 30² + 15² = 3,025 + 900 + 225 = 4,150
- → 컬리 의존도 높음
```

---

## 3. 채널별 상품 믹스 분석

**출처**: Ansoff, H.I. (1957). "Strategies for Diversification". Harvard Business Review (Product-Market Matrix 응용)

### 채널-상품 매트릭스

```
              채널 A    채널 B    채널 C
상품 1          ●         ○         ○       ← 채널 A 강세
상품 2          ○         ●         ○       ← 채널 B 강세
상품 3          ○         ○         ●       ← 채널 C 강세
상품 4          ●         ●         ●       ← 범용 인기 상품

● = 상위 판매, ○ = 하위 판매
```

### 분석 포인트

```
1. 범용 인기 상품: 모든 채널에서 잘 팔리는 상품 → 재고 우선 확보
2. 채널 특화 상품: 특정 채널에서만 잘 팔리는 상품 → 채널 맞춤 프로모션
3. 저성과 상품: 모든 채널에서 부진 → 상품 라인업 재검토
```

---

## 4. 지역별 수요 분석 (Geographic Demand Mapping)

**출처**: Huff, D.L. (1963). "A Probabilistic Analysis of Shopping Center Trade Areas". Land Economics
**발전**: 소매업 상권 분석의 기초 이론

### 온라인 배송지역 분석

```
지역 집중도 = 상위 3개 지역 주문 비중

해석:
- 70% 이상: 수도권 집중형 → 수도권 타깃 마케팅
- 50~70%: 준집중형 → 주요 도시 거점 전략
- 50% 미만: 분산형 → 전국 커버리지 전략
```

### 온라인-오프라인 상권 비교

```
오프라인 상권: 매장 반경 물리적 접근성 (도보/교통)
온라인 상권: 배송지역 = 잠재 고객 위치

비교 인사이트:
- 오프라인 매장이 없는 지역에서 온라인 주문이 많다면?
  → 해당 지역 팝업/오프라인 확장 검토
- 오프라인 매장 주변 지역의 온라인 주문이 많다면?
  → 매장 인지도 → 온라인 전환 패턴
```

---

## 5. 온오프라인 통합 분석 (Omnichannel Analytics)

**출처**: Verhoef, P.C. et al. (2015). "From Multi-Channel Retailing to Omni-Channel Retailing". Journal of Retailing

### 채널 비중 비교

```
온라인 비중 = 온라인 매출 / (온라인 + 오프라인) 매출 x 100

업계 참고:
- 식음료 온라인 비중 평균: 15~25% (2025 기준)
- 기념품/선물 온라인 비중: 30~40%
- 뉴믹스 특성: K-커피 기념품 → 오프라인 관광 구매 비중 높을 것
```

### 채널별 역할 정의

| 역할 | 설명 | 판단 기준 |
|------|------|----------|
| Volume Driver | 매출 규모가 가장 큰 채널 | 매출 1위 |
| Growth Driver | 성장률이 가장 높은 채널 | MoM 성장률 1위 |
| Margin Driver | 수익성이 가장 높은 채널 | 객단가/마진 기준 |
| Acquisition Channel | 신규 고객 유입 채널 | 첫 구매자 비중 |

---

## 6. 프로모션 채널 선택 프레임워크

**출처**: Blattberg, R.C. & Neslin, S.A. (1990). Sales Promotion: Concepts, Methods, and Strategies. Prentice Hall

### 의사결정 매트릭스

```
                    현재 매출 비중
                 높음              낮음
         ┌────────────────┬────────────────┐
    높   │   집중 투자     │   육성 투자    │
 성 음   │ (주력 채널)     │ (성장 채널)    │
 장      ├────────────────┼────────────────┤
 률 낮   │   유지          │   축소 검토    │
    음   │ (효율화)        │ (ROI 재평가)   │
         └────────────────┴────────────────┘
```

---

## 7. 실습 적용 예시

### 프롬프트 템플릿

```
"[온라인 매출 데이터 파일]을 분석해줘.

@channel-mix-framework.md 관점으로:
- 채널별 매출 비중과 객단가 비교
- 채널 집중도(HHI) 계산
- 채널별 인기 상품 교차분석 (채널-상품 매트릭스)
- 배송지역별 주문 분포와 수도권 집중도
- 취소율/반품율 채널별 비교
- 오프라인 대비 온라인 매출 비중"
```

---

## 8. CEO 보고 시 핵심 메시지 구조

```markdown
## 온라인 채널 분석

### 핵심 숫자
- 온라인 총매출: OO만원 (전체 매출의 OO%)
- 1위 채널: OO (매출 OO%, 객단가 OO원)
- 채널 집중도(HHI): OO

### 채널 성과 비교
| 채널 | 매출 | 비중 | 객단가 | 주문 수 | 역할 |
|------|------|------|--------|---------|------|
| | | | | | |

### 지역 수요
- 수도권 비중: OO%
- 주요 비수도권: OO, OO

### So What
- [채널별 핵심 인사이트]

### Now What
- 벚꽃 시즌 프로모션 집중 채널: [추천]
- 이유: [데이터 근거]
```

---

## 참고 자료

- McCarthy, E.J. (1960). Basic Marketing: A Managerial Approach. Richard D. Irwin
- Neslin, S. et al. (2006). Challenges and Opportunities in Multichannel Customer Management. Journal of Service Research
- Verhoef, P.C. et al. (2015). From Multi-Channel Retailing to Omni-Channel Retailing. Journal of Retailing
- Huff, D.L. (1963). A Probabilistic Analysis of Shopping Center Trade Areas. Land Economics
- Blattberg, R.C. & Neslin, S.A. (1990). Sales Promotion. Prentice Hall
- Ansoff, H.I. (1957). Strategies for Diversification. Harvard Business Review
