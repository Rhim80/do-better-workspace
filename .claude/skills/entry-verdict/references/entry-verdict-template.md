# entry-verdict 한 페이지 카드 템플릿

> entry-verdict Step 7에서 사용. zone-report로 HTML/PDF 변환.
> 변수 `{...}`는 entry-verdict가 채움.

---

## 마크다운 카드 (텍스트)

```
┌─────────────────────────────────────────────────────────┐
│ [Verdict: {Go|Conditional|No-Go}] · {zone} {평수}평 · {brand} │
│ 진단일 {date}                                              │
├─────────────────────────────────────────────────────────┤
│ Magnitude (월매출 잠재력)                                  │
│   보수 {p25_revenue}억 · 중립 {p50_revenue}억 · 낙관 {p75_revenue}억   │
│   BEP 임대 {bep_rent}만 │ 시세 {actual_rent}만 │ Δ {delta_pct}%         │
├─────────────────────────────────────────────────────────┤
│ 5-Layer Score                                            │
│   Volume   {bar_volume} {volume_score}                    │
│   Rhythm   {bar_rhythm} {rhythm_score}                    │
│   Pressure {bar_pressure} {pressure_score} {pressure_note}│
│   Concept  {bar_concept} {concept_score}                  │
├─────────────────────────────────────────────────────────┤
│ 7 CQ:  {cq_emojis}  ({pass_count} / {fail_count} / {pending_count})│
│   1. Volume:    {cq1_status} {cq1_note}                  │
│   2. Rhythm:    {cq2_status} {cq2_note}                  │
│   3. Spending:  {cq3_status} {cq3_note}                  │
│   4. Saturation: {cq4_status} {cq4_note}                 │
│   5. Cannibal:  {cq5_status} {cq5_note}                  │
│   6. Concept:   {cq6_status} {cq6_note}                  │
│   7. Magnitude: {cq7_status} {cq7_note}                  │
├─────────────────────────────────────────────────────────┤
│ Toulmin 한 줄: {toulmin_summary}                          │
│ Qualifier: {qualifier}                                    │
│ Rebuttal: {rebuttal}                                      │
├─────────────────────────────────────────────────────────┤
│ 재검토 조건 (Conditional 시):                              │
│   {recheck_conditions}                                    │
├─────────────────────────────────────────────────────────┤
│ 현장 답사 체크리스트:                                       │
│   1. {field_check_1}                                      │
│   2. {field_check_2}                                      │
│   3. {field_check_3}                                      │
│   4. {field_check_4}                                      │
│   5. {field_check_5}                                      │
├─────────────────────────────────────────────────────────┤
│ Sources: {sources_summary}                                │
│ AI 보조 도구. 최종 판단은 사람.                              │
└─────────────────────────────────────────────────────────┘
```

## 비교 매트릭스 (3개 후보 동시)

```
| 항목 | 한남동 | 성수동 | 압구정동 |
|------|--------|--------|----------|
| Verdict | Conditional | Go | No-Go |
| Volume | 7.1 | 8.5 | 6.2 |
| Rhythm | 5.4 | 7.8 | 5.0 |
| Pressure | 6.2 | 5.1 | 7.4 |
| Concept | 8.0 | 7.2 | 6.8 |
| Magnitude Δ% | +31% | +8% | +52% |
| BEP 임대 | 550만 | 880만 | 980만 |
| 시세 | 720만 | 950만 | 1,490만 |
| 7 CQ 충족 | 4 | 6 | 2 |
| 핵심 리스크 | 임대·폐업률 | 컨셉 분화 | 임대 과대 |

추천: **성수동** — 카니발 거리·매출 잠재력·임대 적합성 균형 우수.
한남: 임대 600만 협상 + 70평+ 확장 시 재검토.
압구정: 현 시세 무효, 거리 4km+ 다른 후보지 탐색 권장.
```
