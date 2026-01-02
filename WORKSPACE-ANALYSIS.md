# IMI Workspace 분석 문서

> 작성일: 2025-12-29
> 용도: 워크스페이스 구조 및 기능 설명 (교육용)

## 1. 개요

**imi-workspace**는 비개발자를 위한 AI 작업 환경으로, Claude Code와 Johnny Decimal 시스템을 결합한 실전 PKM(Personal Knowledge Management) 워크스페이스입니다.

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
imi-workspace/
├── .claude/              # Claude Code 확장 기능
│   ├── commands/         # 슬래시 커맨드 (13개)
│   ├── agents/           # 서브에이전트 (3개)
│   └── skills/           # 스킬스 (4개)
├── 00-inbox/             # 빠른 캡처 공간
├── 00-system/            # 시스템 설정 및 템플릿
│   ├── 01-templates/     # 재사용 템플릿 (4개)
│   ├── 02-scripts/       # 자동화 스크립트
│   ├── 03-guides/        # 가이드 문서
│   └── 04-docs/          # 문서
├── 10-projects/          # 활성 프로젝트 (시한부)
│   └── 11-consulting/    # 컨설팅 프레임워크
├── 20-operations/        # 비즈니스 운영 (지속적)
│   └── 21-hr/            # HR/노무 관련
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

## 3. Slash Commands (13개)

### 초기 설정
| 커맨드 | 설명 |
|--------|------|
| `/setup-workspace` | 대화형 CLAUDE.md 자동 생성 + 초기 설정 |
| `/setup-google-calendar` | Google Calendar 연결 (OAuth) |

### Daily Workflow
| 커맨드 | 설명 |
|--------|------|
| `/daily-note` | 오늘 Daily Note 생성/열기 (Google Calendar 자동 통합) |
| `/daily-review` | 어제/오늘 변경사항 분석 |

### 지식 관리
| 커맨드 | 설명 |
|--------|------|
| `/idea [카테고리]` | 대화에서 아이디어 추출 후 PKM에 저장 |
| `/todo` | 할 일 추가 |
| `/todos [today/project/overdue/stats]` | 할 일 목록 조회/관리 |

### AI 활용 (Orchestration)
| 커맨드 | 설명 |
|--------|------|
| `/thinking-partner` | AI와 대화하며 생각 발전 (소크라테스식 질문) |
| `/gather` | 정보 수집 모드 (구조화된 질문 생성) |
| `/reframe` | 이해 확인 모드 (대화 요약 및 확인) |
| `/truth` | 사실 기반 분석 모드 (객관적 분석) |

### 시스템
| 커맨드 | 설명 |
|--------|------|
| `/create-command` | 커스텀 명령어 생성 |

---

## 4. Skills (4개)

### 4.1 Google Calendar
**파일**: `.claude/skills/google-calendar/`

**기능**:
- gcalcli 기반 Google Calendar 통합
- 일정 조회, 검색, 등록, 수정, 삭제
- Daily Note 자동 통합

**트리거 키워드**: "일정", "스케줄", "캘린더"

---

### 4.2 Competitor Review Analyzer
**파일**: `.claude/skills/competitor-review-analyzer/`

**기능**:
- 다나와 상품 리뷰 크롤링
- AI 분석 (긍정/부정/키워드)
- 인사이트 도출 -> 액션 아이템 제안

**트리거 키워드**: "경쟁사 분석", "리뷰 분석", "다나와 리뷰"

---

### 4.3 Notion Handler
**파일**: `.claude/skills/notion-handler/`

**기능**:
- Notion 데이터베이스/페이지 관리
- DB 생성, 페이지 추가

**트리거 키워드**: "노션", "Notion", "DB 만들어", "데이터베이스"

---

### 4.4 Transcript Organizer
**파일**: `.claude/skills/transcript-organizer/`

**기능**:
- 회의/강의 녹취록 정리
- 요점 추출 및 구조화

---

## 5. Agents (서브에이전트, 3개)

### 5.1 Zettelkasten Linker
**파일**: `.claude/agents/zettelkasten-linker.md`

**역할**: PKM vault 종합 분석 및 큐레이션

**기능**:
1. **Quality Assessment**: 파일 품질 평가 (삭제/분할/유지)
2. **Link Suggestion**: 양방향 연결 제안 (>60% 관련성)
3. **Vault Health Report**: 개선 계획 생성

---

### 5.2 Cafe Launch PM
**파일**: `.claude/agents/cafe-launch-pm.md`

**역할**: 카페 브랜드 론칭 프로젝트 관리

**기능**:
- 프로젝트 계획 및 타임라인 관리
- 팀 코디네이션
- 리스크 평가 및 마일스톤 추적

---

### 5.3 YouTube Content Analyzer
**파일**: `.claude/agents/youtube-content-analyzer.md`

**역할**: YouTube 영상 콘텐츠 분석

**기능**:
- 메타데이터 및 트랜스크립트 추출
- 핵심 인사이트 분석
- 콘텐츠 변환 워크플로우 지원

---

## 6. Templates (4개)

| 템플릿 | 용도 |
|--------|------|
| `daily-note-template.md` | 매일 작성하는 노트 (Google Calendar 자동 통합) |
| `weekly-review-template.md` | 주간 회고 |
| `Project Template.md` | 새 프로젝트 시작 |
| `Daily Note Template.md` | (레거시) |

---

## 7. 샘플 데이터 (교육용)

`50-resources/sample-data/` 폴더에 **오피스원 주식회사** 시나리오 기반의 교육용 데이터 포함

### 가상 회사 설정
- **회사명**: 오피스원 주식회사 (OfficeOne Inc.)
- **업종**: B2B 사무용품/사무환경 솔루션
- **규모**: 직원 약 50명, 연매출 약 50억원
- **상황**: 2025년 2분기 종료, 경영 회의 준비

### 데이터셋 현황

| 파일명 | 설명 | 레코드 수 | 주요 컬럼 |
|--------|------|-----------|-----------|
| `sample_sales_data.csv` | 2분기 판매 실적 | 117건 | 날짜, 제품, 고객사, 지역, 수량, 매출, 영업담당 |
| `customer_data.csv` | 고객사 정보 | 50개사 | 회사명, 업종, 지역, 누적매출, 고객상태 |
| `employee_survey_data.csv` | 직원 만족도 설문 | 50명 | 부서, 직급, 만족도 항목별 점수, 근무형태선호 |
| `inventory_data.csv` | 재고 현황 | 40품목 | 제품명, 카테고리, 현재고, 재고상태, 공급업체 |
| `marketing_campaign_data.csv` | 마케팅 캠페인 | 24건 | 캠페인명, 채널, 예산, 매출, ROI |

### 실습 미션 (6개)

| 미션 | 데이터 | 분석 목표 |
|------|--------|-----------|
| 미션 1 | 판매 데이터 | 월별/지역별 매출 추이, 영업담당 실적 |
| 미션 2 | 고객 데이터 | VIP 고객 식별, 비활성 고객 분석 |
| 미션 3 | 마케팅 데이터 | 채널별 ROI 비교, 예산 재배분 제안 |
| 미션 4 | 재고 데이터 | 긴급 발주 품목, 발주 우선순위 |
| 미션 5 | 설문 데이터 | 부서별 만족도, 개선 필요 영역 |
| 미션 6 | 전체 종합 | CEO 보고용 1페이지 요약 |

### 실습 가이드 위치
- **상세 가이드**: `00-system/claude-code-practice-guide.md`
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
│  /daily-note -> Google Calendar Skill -> Daily Note 생성    │
│  /daily-review -> 변경사항 분석 -> 우선순위 제안             │
└─────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────┐
│                ORCHESTRATION COMMANDS                       │
│  /gather -> 정보 수집 (구조화된 질문)                        │
│  /reframe -> 이해 확인 (대화 요약)                          │
│  /truth -> 사실 기반 분석 (객관적 평가)                      │
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
git clone https://github.com/Rhim80/imi-workspace.git
cd imi-workspace

# 2. Claude Code에서 열기
# VS Code 또는 터미널에서 Claude Code 실행

# 3. 초기 설정 (대화형 CLAUDE.md 자동 생성)
/setup-workspace

# 4. (선택) Google Calendar 연결
/setup-google-calendar
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
/gather              # 정보 수집
/reframe             # 이해 확인
/truth               # 사실 기반 분석
```

---

## 10. 기술 스택 요약

| 구성요소 | 기술 |
|----------|------|
| PKM 구조 | Johnny Decimal 시스템 |
| 캘린더 | gcalcli (OAuth) |
| AI 에이전트 | Claude Code Subagents |
| 버전 관리 | Git |

---

## 11. Skills vs Commands vs Agents 비교

| 구분 | Skills | Commands | Agents |
|------|--------|----------|--------|
| **목적** | 외부 서비스 통합 | 내부 워크플로우 자동화 | 복잡한 다단계 작업 |
| **예시** | Google Calendar, Notion | `/daily-note`, `/todos` | Zettelkasten Linker |
| **위치** | `.claude/skills/` | `.claude/commands/` | `.claude/agents/` |
| **설정** | OAuth, API 키 필요 | 설정 불필요 (즉시 사용) | 설정 불필요 |
| **호출** | 키워드 자동 감지 | `/command` 형식 | 자연어 요청 |

---

## 12. 주요 특징 요약

1. **비개발자 친화적**: CLI 환경이지만 자연어로 대화하며 사용
2. **대화형 설정**: `/setup-workspace`로 CLAUDE.md 자동 생성
3. **체계적 구조**: Johnny Decimal로 AI가 이해하기 쉬운 폴더 구조
4. **Orchestration Commands**: gather, reframe, truth로 체계적 사고
5. **Daily Workflow 자동화**: 캘린더, Todo, 리뷰가 유기적으로 연결
6. **확장 가능**: Skills, Commands, Agents로 기능 확장 용이

---

**Made with Claude Code by hovoo (이림)**
F&B Professional x AI Practitioner
