# 마케팅 ROI 분석 프레임워크

> 기반: ROAS/CPA Analysis, Marketing Efficiency Ratio, Budget Allocation Optimization

---

## 1. 핵심 성과 지표 (KPI)

**출처**: Lenskold, J. (2003). Marketing ROI: The Path to Campaign, Customer, and Corporate Profitability. McGraw-Hill

### 기본 KPI

| KPI | 공식 | 의미 | 벤치마크 |
|-----|------|------|----------|
| ROAS | 매출기여 / 집행비용 | 광고 1원당 매출 | 3.0x 이상 양호 |
| CPA | 집행비용 / 전환수 | 전환 1건당 비용 | 업종별 상이 |
| CTR | 클릭수 / 노출수 x 100 | 광고 클릭률 | 디스플레이 0.5~2%, 검색 3~8% |
| CVR | 전환수 / 클릭수 x 100 | 클릭 후 구매율 | 1~5% (e-commerce) |
| CPM | 집행비용 / 노출수 x 1000 | 노출 1천회당 비용 | 채널별 상이 |

### 심화 KPI

| KPI | 공식 | 의미 |
|-----|------|------|
| MER (Marketing Efficiency Ratio) | 총매출 / 총마케팅비 | 전사 마케팅 효율 |
| iROAS (incremental ROAS) | 증분매출 / 집행비용 | 광고가 없었으면 안 생겼을 매출 |
| CAC (Customer Acquisition Cost) | 총마케팅비 / 신규고객수 | 고객 1명 획득 비용 |
| LTV:CAC | 고객생애가치 / 획득비용 | 3:1 이상 건전 |

---

## 2. 채널별 ROAS 비교

**출처**: Berman, R. (2018). "Beyond the Last Touch: Attribution in Online Advertising". Marketing Science

### 채널별 벤치마크 (패션 e-commerce)

| 채널 | ROAS 범위 | 특성 |
|------|-----------|------|
| 네이버 SA | 5~10x | 검색 의도 높음, 전환율 우수 |
| 메타 (인스타/FB) | 3~6x | 볼륨 최대, 타깃팅 정교 |
| 구글 | 3~6x | 리마케팅 강점, 쇼핑광고 |
| 카카오 | 2~5x | 국내 도달, 친구톡/알림톡 |
| 틱톡 | 2~5x | 젊은층 도달, 성장세 |
| 유튜브 | 2~4x | 브랜딩+퍼포먼스 혼합 |

### 채널 효율 매트릭스

```
                   ROAS (효율)
                높음              낮음
         +----------------+----------------+
    볼   |   Star          |   Question     |
    륨   | 집중 투자        | Mark           |
    (    | (핵심 채널)      | (효율 개선 후  |
    매   |                  |  스케일업)      |
    출   +----------------+----------------+
    기   |   Cash Cow      |   Dog          |
    여   | 효율 유지         | 축소 검토      |
    )    | (최적화 집중)     | (ROI 재평가)   |
         +----------------+----------------+
```

---

## 3. 캠페인 유형별 분석

**출처**: Sharp, B. (2010). How Brands Grow. Oxford University Press

### 유형별 기대 성과

| 유형 | 목적 | ROAS 기대 | 주요 KPI |
|------|------|-----------|----------|
| 브랜딩 | 인지도/고려도 | 1.5~3x | 도달, VTR, 브랜드리프트 |
| 퍼포먼스 | 전환/매출 | 3~7x | ROAS, CPA, CVR |
| 리타겟팅 | 이탈 복귀 | 8~15x | ROAS 높지만 볼륨 제한 |
| CRM | 기존고객 활성화 | 5~12x | 재구매율, LTV |

### 퍼널별 역할

```
인지 (Awareness)     ← 브랜딩 캠페인
  ↓
고려 (Consideration) ← 퍼포먼스 캠페인
  ↓
전환 (Conversion)    ← 리타겟팅 캠페인
  ↓
충성 (Loyalty)       ← CRM 캠페인

주의: 리타겟팅 ROAS가 높다고 리타겟팅만 늘리면?
→ 상위 퍼널(인지/고려) 축소 → 리타겟팅 모수 감소 → 전체 매출 하락
→ 퍼널 밸런스가 핵심
```

---

## 4. 예산 배분 최적화

**출처**: Naik, P.A. & Raman, K. (2003). "Understanding the Impact of Synergy in Multimedia Communications". Journal of Marketing Research

### 배분 원칙

```
1. 효율 기반 배분 (Efficiency-based)
   각 채널 예산 = 총예산 x (채널 ROAS / 전체 ROAS 합)
   → 한계: 리타겟팅에 과도 집중 우려

2. 역할 기반 배분 (Role-based)
   브랜딩 20~30% + 퍼포먼스 40~50% + 리타겟팅 15~20% + CRM 10~15%
   → 퍼널 밸런스 유지

3. 하이브리드 배분 (권장)
   역할별 예산 먼저 배분 → 역할 내에서 ROAS 기반 채널 배분
```

### 시뮬레이션 접근

```
현재 배분:  메타 40% / 네이버 25% / 구글 15% / 카카오 10% / 틱톡 5% / 유튜브 5%
현재 성과:  총 ROAS 4.2x

최적화안:   메타 35% / 네이버 30% / 구글 12% / 카카오 8% / 틱톡 10% / 유튜브 5%
예상 성과:  총 ROAS 4.8x (+14%)

변경 이유:
- 네이버SA ROAS 최고 → 비중 확대
- 틱톡 CPA 개선 추세 → 테스트 예산 증가
- 메타 볼륨 포화 → 소폭 축소
```

---

## 5. MoM (전월 대비) 분석

### 비교 포인트

```
1. 총 마케팅비: 증감 + 이유 (시즌, 캠페인, 이벤트)
2. 총 ROAS: 효율 변화 + 원인 (크리에이티브, 타깃, 경쟁)
3. 채널별 ROAS 변동: 어떤 채널이 좋아졌고/나빠졌는지
4. CPA 추이: 전환 비용이 오르고 있는지/내리고 있는지
5. 계절성 보정: 설 연휴, 시즌오프 등 외부 요인 제거
```

---

## 6. 실습 적용 예시

### 프롬프트 템플릿

```
"[매체비 데이터]와 [캠페인 성과 데이터]를 분석해줘.

@marketing-roi-framework.md 관점으로:
- 매체별 ROAS, CPA, CTR, CVR 계산 후 비교
- 캠페인유형별(브랜딩/퍼포먼스/리타겟팅/CRM) 효율 분석
- 채널 효율 매트릭스 (ROAS x 볼륨) 그려줘
- 일별 집행 추이와 효율 변동
- 다음 달 예산 [금액] 기준 채널별 최적 배분 추천
- So What / Now What 정리"
```

---

## 7. CMO 보고 시 핵심 메시지 구조

```markdown
## 마케팅 ROI 분석

### 핵심 숫자
- 2월 총 마케팅비: OO억 (MoM OO%)
- 전체 ROAS: OO배 (MoM OO%)
- 최고 효율 채널: OO (ROAS OO배)

### 채널별 성과 비교
| 채널 | 집행비 | ROAS | CPA | 매출기여 | 판단 |
|------|--------|------|-----|----------|------|
| | | | | | |

### 캠페인 유형별 효율
| 유형 | ROAS | CPA | 비중 | 진단 |
|------|------|-----|------|------|
| | | | | |

### So What
- [효율/비효율 채널 인사이트]
- [퍼널 밸런스 진단]

### Now What
- 3월 예산 OO억 배분안: [채널별 비중]
- 근거: [데이터 기반 이유]
```

---

## 참고 자료

- Lenskold, J. (2003). Marketing ROI. McGraw-Hill
- Berman, R. (2018). Beyond the Last Touch. Marketing Science
- Sharp, B. (2010). How Brands Grow. Oxford University Press
- Naik, P.A. & Raman, K. (2003). Understanding the Impact of Synergy in Multimedia Communications. JMR
