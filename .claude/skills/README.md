# Skills

> Claude Code와 외부 서비스를 통합하는 기능 모음

## 사용 가능한 Skills

### web-crawler-ocr/

웹페이지 크롤링 + 이미지 OCR 처리 (Firecrawl + Gemini):
- Firecrawl로 깨끗한 텍스트 추출 (광고/잡음 제거)
- Gemini OCR로 대용량 이미지 처리 (20MB, Claude 5MB 제한 우회)
- URL 자동 감지 및 실행

자세한 내용: [web-crawler-ocr/README.md](./web-crawler-ocr/README.md)

### transcript-organizer/

녹음 텍스트 파일(강의, 미팅, 인터뷰) 분석 및 구조화:
- 인코딩 자동 감지(UTF-16 -> UTF-8), STT 오인식 교정
- 유형별 템플릿 적용 (강의/미팅/인터뷰)

### notion-handler/

Notion 데이터베이스 및 페이지 관리:
- 데이터베이스 조회/생성/업데이트
- 페이지 블록 타입 확장 및 관리

### dashboard-prd/

대시보드 PRD 대화형 생성:
- 결정 우선(Decision-First) 원칙 기반 설계
- 4단계 대화형 프로세스 (의사결정 -> 데이터 -> 화면 -> 기술)

### excel-to-csv/

Excel 파일을 Claude Code에서 분석 가능한 CSV로 변환:
- 멀티 시트 지원, EUC-KR 인코딩 변환
- .xlsx 파일 경로 제공 시 자동 실행

### csv-clean/

CSV 데이터 품질 정리:
- 소계행 제거, 숫자 정리, 날짜 정규화, unpivot
- "데이터 정리", "CSV 정리" 등 키워드로 자동 실행

---

## Skills vs Commands

| 구분 | Skills | Commands |
|------|--------|----------|
| **목적** | 외부 서비스 통합 | 내부 워크플로우 자동화 |
| **예시** | web-crawler-ocr, notion-handler | `/daily-note`, `/setup-workspace` |
| **설정** | API 키 필요 (경우에 따라) | 설정 불필요 (즉시 사용) |

---

## 커스텀 Skills 추가

### 1. 폴더 생성
```bash
mkdir -p skills/skill-name/scripts
```

### 2. SKILL.md 작성
```markdown
---
name: skill-name
description: 스킬 설명 및 트리거 키워드
allowed-tools: Bash, Read
---
```

### 3. 참고 자료
- 예시: [web-crawler-ocr/](./web-crawler-ocr/) 폴더 구조 참고
