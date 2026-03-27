# Do Better Workspace 분석 문서

> 작성일: 2025-12-29
> 용도: 워크스페이스 구조 및 기능 설명 (교육용)

## 1. 개요

**do-better-workspace**는 비개발자를 위한 AI 작업 환경으로, Claude Code와 Johnny Decimal 시스템을 결합한 실전 PKM(Personal Knowledge Management) 워크스페이스입니다.

**용도**: Claude Code + PKM 시스템 교육용으로 제작

**핵심 철학**:
1. AI amplifies thinking, not just writing
2. File system = AI memory
3. Structure enables creativity
4. Iteration over perfection
5. Immediate usability

---

## 2. 폴더 구조 (Johnny Decimal 시스템)

```
do-better-workspace/
├── .claude/              # Claude Code 확장 기능
│   ├── commands/         # 슬래시 커맨드 (8개)
│   ├── agents/           # 서브에이전트 (2개)
│   └── skills/           # 스킬스 (6개)
├── 00-inbox/             # 빠른 캡처 공간
├── 00-system/            # 시스템 설정 및 템플릿
│   ├── 01-templates/     # 기본 노트 템플릿 (3개)
│   ├── 02-scripts/       # 자동화 스크립트
│   ├── 03-guides/        # 가이드 문서
│   └── 04-docs/          # 문서
├── 10-projects/          # 활성 프로젝트 (시한부)
├── 20-operations/        # 비즈니스 운영 (지속적)
├── 30-knowledge/         # 지식 아카이브
├── 40-personal/          # 개인 노트
│   ├── 41-daily/         # Daily Notes
│   ├── 42-weekly/        # Weekly Reviews
│   ├── 45-ideas/         # 아이디어
│   └── 46-todos/         # 할 일 관리
├── 50-resources/         # 참고 자료
└── 90-archive/           # 완료/중단 항목
```

---

## 3. Slash Commands

### 초기 설정
| 커맨드 | 설명 |
|--------|------|
| `/setup-workspace` | 대화형 CLAUDE.md 자동 생성 + 초기 설정 |

### Daily Workflow
| 커맨드 | 설명 |
|--------|------|
| `/daily-note` | 오늘 Daily Note 생성/열기 |
| `/daily-review` | 어제/오늘 변경사항 분석 |

### 지식 관리
| 커맨드 | 설명 |
|--------|------|
| `/idea [카테고리]` | 대화에서 아이디어 추출 후 PKM에 저장 |
| `/todo` | 할 일 추가 |
| `/todos [today/project/overdue/stats]` | 할 일 목록 조회/관리 |

### AI 활용
| 커맨드 | 설명 |
|--------|------|
| `/thinking-partner` | AI와 대화하며 생각 발전 (소크라테스식 질문) |

### 시스템
| 커맨드 | 설명 |
|--------|------|
| `/create-command` | 커스텀 명령어 생성 |

---

## 4. Skills (6개)

- **csv-clean** - CSV 데이터 품질 정리
- **dashboard-prd** - 대시보드 PRD 대화형 생성
- **excel-to-csv** - Excel 파일을 CSV로 변환
- **notion-handler** - Notion 데이터베이스/페이지 관리
- **transcript-organizer** - 회의/강의 녹취록 정리
- **web-crawler-ocr** - 웹페이지 크롤링 + 이미지 OCR

---

## 5. Agents (서브에이전트, 2개)

- **research-worker** - 웹 리서치 및 정보 수집 (다국어 검색, 교차 검증)
- **zettelkasten-linker** - PKM vault 종합 분석 및 큐레이션

---

## 6. Templates (3개)

| 템플릿 | 용도 |
|--------|------|
| `daily-note-template.md` | 매일 작성하는 노트 |
| `weekly-review-template.md` | 주간 회고 |
| `Project Template.md` | 새 프로젝트 시작 |

> 데이터 분석용 프레임워크 템플릿은 클라이언트별 브랜치에 포함되어 있습니다.

---

## 7. 샘플 데이터 (교육용)

교육용 샘플 데이터는 클라이언트별 브랜치에서 제공됩니다. `main` 브랜치에는 포함되어 있지 않습니다.

| 브랜치 | 업종 | 데이터 유형 |
|--------|------|------------|
| `ax/newmix` | F&B (카페) | 매장 매출, 온라인 매출, 재고 현황 |
| `ax/musinsa` | 패션 플랫폼 | 캠페인 성과, 인플루언서, 미디어, SNS |
| `ax/royal` | 제조업 (욕실) | B2B 주문, 온라인 매출, 재고 |
| `ax/gardeningclub` | 커뮤니티 | 인스타그램, 프로젝트, 식물 DB |

각 브랜치에는 데이터, 분석 프레임워크 템플릿, 실습 시나리오가 포함되어 있습니다.

### 실습 가이드 위치
- **기본 가이드**: `00-system/claude-code-practice-guide.md`
- **데이터 설명**: `50-resources/sample-data/README.md`

---

## 8. 핵심 기능 연결도

```
┌─────────────────────────────────────────────────────────────┐
│                    INITIAL SETUP                            │
│  /setup-workspace -> 대화형 정보 수집 -> CLAUDE.md 자동 생성 │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│                    DAILY WORKFLOW                           │
│  /daily-note -> Daily Note 생성                             │
│  /daily-review -> 변경사항 분석 -> 우선순위 제안             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│                AI 활용                                      │
│  /thinking-partner -> 소크라테스식 대화                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│                KNOWLEDGE MANAGEMENT                         │
│  /idea -> 대화에서 인사이트 추출 -> 30-knowledge 저장        │
│  /todos -> 할 일 관리 -> active-todos.md                    │
│  Zettelkasten Linker -> 노트 연결 및 품질 관리              │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. 사용자 시작 가이드

### 최초 설정 (5분)
```bash
# 1. Clone
git clone https://github.com/Rhim80/do-better-workspace.git
cd do-better-workspace

# 2. Claude Code에서 열기
# VS Code 또는 터미널에서 Claude Code 실행

# 3. 초기 설정 (대화형 CLAUDE.md 자동 생성)
/setup-workspace

```

### 매일 사용
```bash
/daily-note          # 아침: 오늘 계획
/todos today         # 오늘 할 일 확인
/daily-review        # 저녁: 하루 정리
```

### 생각 정리가 필요할 때
```bash
/thinking-partner    # 소크라테스식 대화
```

---

## 10. 기술 스택 요약

| 구성요소 | 기술 |
|----------|------|
| PKM 구조 | Johnny Decimal 시스템 |
| AI 에이전트 | Claude Code Subagents |
| 버전 관리 | Git |

---

## 11. Skills vs Commands vs Agents 비교

| 구분 | Skills | Commands | Agents |
|------|--------|----------|--------|
| **목적** | 외부 서비스 통합 | 내부 워크플로우 자동화 | 복잡한 다단계 작업 |
| **예시** | Web Crawler, Notion | `/daily-note`, `/todos` | Zettelkasten Linker |
| **위치** | `.claude/skills/` | `.claude/commands/` | `.claude/agents/` |
| **설정** | OAuth, API 키 필요 | 설정 불필요 (즉시 사용) | 설정 불필요 |
| **호출** | 키워드 자동 감지 | `/command` 형식 | 자연어 요청 |

---

## 12. 주요 특징 요약

1. **비개발자 친화적**: CLI 환경이지만 자연어로 대화하며 사용
2. **대화형 설정**: `/setup-workspace`로 CLAUDE.md 자동 생성
3. **체계적 구조**: Johnny Decimal로 AI가 이해하기 쉬운 폴더 구조
4. **AI 활용**: thinking-partner로 체계적 사고
5. **Daily Workflow 자동화**: Todo, 리뷰가 유기적으로 연결
6. **확장 가능**: Skills, Commands, Agents로 기능 확장 용이

---

**Made with Claude Code by hovoo (이림)**
F&B Professional x AI Practitioner
