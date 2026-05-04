---
name: zone-report
description: zone-diagnosis 또는 entry-verdict 결과를 한 페이지 HTML/PDF 카드로 출력. md-to-pdf 변형. "리포트 만들어", "PDF 출력", "한 페이지 카드" 등 언급 시 자동 실행.
---

# zone-report — 한 페이지 카드 출력 (PDF로 뽑기)

> **한 줄**: 진단·판정 결과를 한 페이지 PDF 카드로 출력. 발표·공유·인쇄용.
> **언제 씀**: `zone-diagnosis` 또는 `entry-verdict` 결과가 나온 후, 들고 다닐 카드가 필요할 때.
> **출력**: `50-resources/data/reports/{type}-{zone}-{YYYYMMDD}.{html,pdf}`

---

## 사장님 입장에서 보면

**이게 뭘 해주나요?**
진단·판정 결과를 한 페이지 PDF 카드로 뽑아줍니다. 들고 다니거나 팀에 공유할 한 장.

**이럴 때 쓰세요**
- "오늘 분석 결과 들고 다닐 카드 한 장 필요해"
- "팀에 공유할 자료"
- "발표·회의에서 한 장 띄울 거"
- "Conditional 판정 받았는데 부동산 협상용 자료로"

**결과로 손에 쥐는 것**
- A4 1페이지 PDF (DBT Deep Forest 디자인 — Cream 배경 + Forest 헤더)
- HTML 버전도 같이 (편집·웹 공유 시)
- 진단 카드 / 판정 카드 / 비교 매트릭스(3개 후보) 자동 선택

**주의**
- 한 페이지 초과 시 자동 축소. 가독성 한계 있으면 진행자 수동 트림.
- 비교 매트릭스(3개 후보)는 가로 레이아웃 권장.
- 인쇄 시 배경색 옵션 ON.

---

## 입력

다음 중 하나:
- `50-resources/data/diagnosis-{zone}-{date}.md` (zone-diagnosis 출력)
- `50-resources/data/verdict-{zone}-{date}.md` (entry-verdict 출력)
- `50-resources/data/verdict-comparison-{date}.md` (3개 비교 매트릭스)

## 프로세스

### Step 1 — 입력 종류 판별

파일명 또는 frontmatter로 type 판별 (diagnosis / verdict / comparison).

### Step 2 — 템플릿 선택

| Type | 템플릿 |
|------|--------|
| diagnosis | `zone-diagnosis/references/diagnosis-template.md` |
| verdict | `entry-verdict/references/entry-verdict-template.md` |
| comparison | 비교 매트릭스 (entry-verdict-template.md 후반부) |

### Step 3 — 마크다운 → HTML 변환

`md-to-pdf` 스킬 패턴 차용:
- DBT Deep Forest 테마 (기본)
- A4 세로 1페이지
- pandoc 또는 markdown-it + custom CSS
- 페이지 overflow 자동 방지 (font-size 자동 축소)

### Step 4 — Chrome headless로 PDF 변환

```bash
chromium --headless --disable-gpu --no-sandbox --print-to-pdf={output.pdf} {output.html}
```

### Step 5 — 출력

- `50-resources/data/reports/{type}-{zone}-{YYYYMMDD}.html`
- `50-resources/data/reports/{type}-{zone}-{YYYYMMDD}.pdf`

## 카드 디자인 (DBT Deep Forest)

- **배경**: Cream (#F5F1E8)
- **헤더**: Forest (#2E4F3E) 띠 + 흰색 타이틀
- **데이터 강조**: Muted Red (#A05656) — 미충족·경고
- **충족 마크**: Forest 진한 톤
- **푸터**: 회색 작은 글씨로 면책 + 출처

## 체크리스트

- 입력 파일에 frontmatter (type 표시) 있나?
- DBT Deep Forest CSS 로드되나?
- A4 1페이지 안에 들어가는가? (overflow 시 자동 축소)
- Chrome headless 설치 확인

## 주의

- 한 페이지 초과 시 자동 축소되지만 가독성 한계. 필요 시 진행자 수동 트림.
- 비교 매트릭스(3개 후보)는 가로 레이아웃 권장.
- PDF 인쇄 시 색상 유지 (배경색 인쇄 옵션 ON).

## 참고

- md-to-pdf 스킬 (전역) — 변환 코어 패턴
- entry-verdict-template.md / diagnosis-template.md (카드 구조)
- DBT Deep Forest 테마 — md-to-pdf의 references/ 참조
