# Agents

> Claude Code Subagents for advanced automation

## Available Agents

### zettelkasten-linker.md

PKM vault 전체 분석 및 품질/연결 개선:
- 삭제/분리/유지 파일 판단 (Quality Assessment)
- 노트 간 양방향 연결 제안 (Link Suggestions)
- 실행 계획 포함 Vault Health Report 생성

**사용 시점**:
- vault 파일이 50개 이상으로 늘었을 때
- 고립된 노트(링크 없음)가 많을 때
- 저품질 파일 정리가 필요할 때

**호출 방법**: 자연어로 요청
```
"내 PKM vault 분석해서 노트 간 연결 제안해줘"
"삭제하거나 분리할 파일 찾아줘"
```

설정 상세: `zettelkasten-linker.md` 참고 (품질 임계값, 링크 신뢰도, 제외 패턴)

### research-worker.md

웹 리서치 및 정보 수집 자동화:
- 한국어/영어 동시 검색, 3개 이상 독립 소스 교차 검증
- 시장 조사, 경쟁사 분석, 문서 리뷰, 팩트체크에 활용

**호출 방법**: 자연어로 요청
```
"이 주제에 대한 자료 조사해줘"
"경쟁사 랜딩페이지 분석해줘"
```

---

## 커스텀 Agent 추가

### 파일 생성 위치
이 폴더에 `.md` 파일 추가

### 템플릿
```yaml
---
name: my-agent-name
description: Claude가 이 agent를 사용할 시점에 대한 설명
model: sonnet
color: blue
---

You are [agent role and expertise].

## Core Mission
[What this agent does]

## Process
[Step-by-step workflow]

## Output Format
[What the agent returns]
```

### Agent 설계 원칙
1. Single Responsibility: 하나의 agent = 하나의 역할
2. Clear Output: 반환값을 명확히 정의
3. Configurable: 파라미터를 설정 섹션으로 분리
