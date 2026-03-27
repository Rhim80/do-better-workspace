# Do Better Workspace

> AI-powered workspace for non-coders
> 비개발자를 위한 AI 작업 환경

---

## What is Do Better Workspace?

Claude Code와 Johnny Decimal 시스템을 결합한 **실전 PKM 워크스페이스**입니다.

**핵심 특징:**
- 15년 F&B 경력 + AI 활용 전문가의 **실제 운영 시스템** 기반
- 강의/워크숍용으로 정리된 **교육용 버전**
- 바로 clone해서 사용 가능한 **즉시 활용형** 구조

> 이 레포지토리는 이림(hovoo)이 실제로 사용하는 PKM 시스템을 교육용으로 정리한 버전입니다.
> Daily Note, Todo 관리, 프로젝트 구조화 등 모든 기능이 실제 업무에서 검증된 것들입니다.

## Quick Start (5분)

### 1. Clone
```bash
git clone https://github.com/Rhim80/do-better-workspace.git
cd do-better-workspace
```

### 2. Claude Code에서 열기
VS Code 또는 터미널에서 Claude Code 실행

### 3. 초기 설정 (핵심!)
```bash
/setup-workspace
```
**대화형으로 CLAUDE.md를 자동 생성**합니다:
- 이름, 역할, 관심사, 용도를 순서대로 질문
- 답변을 기반으로 CLAUDE.md 파일 자동 생성
- 첫 Daily Note 생성
- 다음 단계 안내

### 4. 핵심 커맨드 익히기

| 커맨드 | 용도 |
|--------|------|
| `/daily-note` | 오늘의 Daily Note 생성 |
| `/thinking-partner` | 생각 정리 파트너 |
| `/todos` | 할 일 관리 |

## Philosophy

1. **AI amplifies thinking**, not just writing
2. **File system = AI memory**
3. **Structure enables creativity**
4. **Iteration over perfection**
5. **Immediate usability**

## Folder Structure

Johnny Decimal 시스템 기반 - **AI가 이해하기 쉬운 구조**

```
do-better-workspace/
├── .claude/
│   ├── agents/        # AI 에이전트 (zettelkasten-linker)
│   ├── commands/      # 슬래시 커맨드 8개
│   └── skills/        # 프로젝트 스킬 5개
├── 00-inbox/          # 빠른 캡처 공간
├── 00-system/         # 시스템 설정 및 템플릿
│   ├── 01-templates/  # 기본 노트 템플릿 3개
│   ├── 02-scripts/    # 자동화 스크립트
│   ├── 03-guides/     # 가이드 3개
│   ├── 04-docs/       # 문서 (Johnny Decimal 가이드, 세션 노트)
│   ├── claude-code-practice-guide.md
│   ├── git-setup-guide.md
│   └── notion-setup-guide.md
├── 10-projects/       # 활성 프로젝트 (시한부)
├── 20-operations/     # 비즈니스 운영 (지속적)
├── 30-knowledge/      # 지식 아카이브
│   └── 37-claude-code/ # Claude Code 관련 지식
├── 40-personal/       # 개인 노트
│   ├── 41-daily/      # Daily Notes (월별 하위 폴더)
│   ├── 42-weekly/     # Weekly Reviews
│   ├── 45-ideas/      # 아이디어
│   └── 46-todos/      # 할 일 관리
├── 50-resources/      # 참고 자료
│   └── sample-data/   # 교육용 샘플 데이터 (브랜치별 제공)
└── 90-archive/        # 완료/중단 항목
```

### Johnny Decimal 시스템 이해하기

#### 기본 원칙
- **10단위 = 카테고리** (예: 10-projects, 20-operations)
- **1단위 = 하위 폴더** (예: 11-xxx, 12-xxx)
- **명확한 숫자 = 빠른 탐색**

#### 네이밍 규칙
```
[숫자]-[설명적-이름]

예시:
✅ 11-imi-cafe-project
✅ 21-daily-store-operations
✅ 31-business-frameworks
❌ my-project (숫자 없음)
❌ 11project (하이픈 없음)
```

### 각 카테고리 상세 설명

#### 00-inbox (빠른 캡처)
**용도**: 생각나는 즉시 기록
- 아이디어
- 링크
- 빠른 메모

**관리**: 주 1회 정리하여 적절한 폴더로 이동

---

#### 00-system (시스템 설정)
**용도**: 워크스페이스 설정 및 템플릿
- `01-templates/` - 기본 노트 템플릿 (Daily Note, Weekly Review, Project)
- `02-scripts/` - 자동화 스크립트
- `03-guides/` - 가이드 문서 3개
- `04-docs/` - 참고 문서 (Johnny Decimal 가이드, 세션 노트)
- `claude-code-practice-guide.md` - Claude Code 실습 가이드
- `git-setup-guide.md` - Git 설정 가이드
- `notion-setup-guide.md` - Notion 연동 가이드

**수정 가능**: 필요에 따라 템플릿 커스터마이징

> 데이터 분석용 프레임워크 템플릿은 클라이언트별 브랜치에 포함되어 있습니다.

---

#### 10-projects (시한부 프로젝트)
**용도**: 시작일과 종료일이 있는 프로젝트
**특징**: 완료되면 90-archive로 이동

**하위 폴더 생성 예시**:
```
10-projects/
├── 11-website-redesign/
│   ├── README.md
│   ├── requirements.md
│   └── progress.md
├── 12-product-launch/
└── 13-marketing-campaign/
```

**네이밍 팁**:
- 11~19 사이 숫자 사용
- 프로젝트명은 구체적으로
- 완료되면 `90-archive/`로 이동

---

#### 20-operations (지속적 운영)
**용도**: 반복적이고 지속적인 업무
**특징**: 종료일 없이 계속 유지

**하위 폴더 생성 예시**:
```
20-operations/
├── 21-hr/
├── 22-team-management/
└── 23-customer-service/
```

**네이밍 팁**:
- 21~29 사이 숫자 사용
- 반복적 업무 중심
- 프로세스 문서화

---

#### 30-knowledge (지식 아카이브)
**용도**: 검증된 지식과 학습 자료
**특징**: 재사용 가능한 인사이트

**하위 폴더 생성 예시**:
```
30-knowledge/
├── 31-business/
├── 32-business-frameworks/
│   ├── lean-canvas.md
│   └── okr-system.md
├── 37-claude-code/
└── 38-industry-insights/
```

**네이밍 팁**:
- 31~39 사이 숫자 사용
- 주제별로 분류
- 검증된 내용만 저장

---

#### 40-personal (개인 노트)
**용도**: 개인적인 기록과 회고
**특징**: 날짜 기반 파일명

**구조**:
```
40-personal/
├── 41-daily/
│   └── 2026-03/
│       ├── 2026-03-01.md
│       └── 2026-03-17.md
├── 42-weekly/
│   └── 2026-W11.md
├── 45-ideas/
│   └── (아이디어 저장)
└── 46-todos/
    └── active-todos.md
```

**파일명 규칙**:
- Daily: `YYYY-MM-DD.md` (월별 폴더로 관리)
- Weekly: `YYYY-WXX.md`

---

#### 50-resources (참고 자료)
**용도**: 외부 자료 저장
- PDF, 이미지
- 다운로드한 문서
- 참고 링크 모음

---

#### 90-archive (아카이브)
**용도**: 완료/중단된 프로젝트
**관리**: 분기별로 정리

**구조 예시**:
```
90-archive/
├── 2025-Q4/
│   ├── 11-website-redesign/
│   └── 12-product-launch/
└── 2026-Q1/
```

## Templates

`00-system/01-templates/`에서 사용 가능한 기본 템플릿:

- **daily-note-template.md** - 매일 작성하는 노트
- **weekly-review-template.md** - 주간 회고
- **Project Template.md** - 새 프로젝트 시작

> 데이터 분석용 프레임워크 템플릿(매출 분석, 재고 관리, 마케팅 ROI 등)은 클라이언트별 브랜치에 포함되어 있습니다.

## Slash Commands

`.claude/commands/`에서 사용 가능한 커맨드 (8개):

### 초기 설정
- `/setup-workspace` - **대화형 CLAUDE.md 자동 생성** + 초기 설정

### Daily Workflow
- `/daily-note` - 오늘 날짜의 Daily Note 생성/열기
- `/daily-review` - 어제와 오늘 변경사항 분석
- `/todo` - 빠른 할 일 추가
- `/todos` - 할 일 목록 조회 및 관리

### Thinking & Ideas
- `/thinking-partner` - 생각 정리 파트너 (소크라테스식 질문)
- `/idea` - 대화에서 아이디어 추출 및 저장

### 시스템
- `/create-command` - 커스텀 명령어 생성

### 프로젝트 스킬 및 에이전트

`.claude/skills/`에 이 워크스페이스 전용 스킬 6개가 포함되어 있습니다:

- **csv-clean** - CSV 데이터 품질 정리 (소계 제거, 날짜 정규화 등)
- **dashboard-prd** - 대시보드 PRD 대화형 생성
- **excel-to-csv** - Excel 파일을 CSV로 변환하여 분석 가능하게 만듦
- **notion-handler** - Notion 데이터베이스/페이지 관리
- **transcript-organizer** - 강의/미팅 녹음 텍스트 구조화
- **web-crawler-ocr** - 웹페이지 크롤링 + 이미지 OCR 분석

`.claude/agents/`에 에이전트 2개가 포함되어 있습니다:

- **research-worker** - 웹 리서치 및 정보 수집 (다국어 검색, 교차 검증)
- **zettelkasten-linker** - 노트 간 연결 자동 생성 (Zettelkasten 방식)

> 프로젝트 스킬은 이 워크스페이스에서만 적용되며, 전역 스킬(`~/.claude/skills/`)과 독립적으로 작동합니다.

## 대화형으로 Claude와 작업하기

**예시 1: 프로젝트 생성**
```
You: "매장 운영 체크리스트를 만들고 싶어. 어디에 저장하면 좋을까?"

Claude: "20-operations/21-daily-store-management/ 폴더를 만들고
opening-checklist.md와 closing-checklist.md를 생성하는 것을 추천합니다."
```

**예시 2: 폴더 정리**
```
You: "inbox에 있는 아이디어들을 정리하고 싶어."

Claude: "inbox 파일들을 확인하고 각각 적절한 위치로 이동시켜드리겠습니다.
- 프로젝트 아이디어 → 10-projects/
- 학습 메모 → 30-knowledge/
- 개인 일기 → 40-personal/41-daily/에 통합"
```

**예시 3: 구조 질문**
```
You: "고객 관리 프로세스 문서는 어디에 넣어야 해?"

Claude: "지속적인 업무이므로 20-operations/23-customer-service/
폴더를 만들어서 저장하는 것이 좋습니다."
```

## Sample Data for Practice

교육용 샘플 데이터는 **클라이언트별 브랜치**에서 제공됩니다.

| 브랜치 | 업종 | 데이터 |
|--------|------|--------|
| `ax/newmix` | F&B (카페) | 매장 매출, 온라인 매출, 재고 현황 |
| `ax/musinsa` | 패션 플랫폼 | 캠페인 성과, 인플루언서, 미디어, SNS |
| `ax/royal` | 제조업 (욕실) | B2B 주문, 온라인 매출, 재고 |
| `ax/gardeningclub` | 커뮤니티 | 인스타그램, 프로젝트, 식물 DB |

```bash
# 특정 클라이언트 데이터로 실습하려면
git checkout ax/newmix
```

각 브랜치에는 해당 업종에 맞는 분석 프레임워크 템플릿과 실습 시나리오가 포함되어 있습니다.

### 실습 가이드

`00-system/claude-code-practice-guide.md`에서 기본 실습(환경 설정, 폴더 정리)을 진행한 후, 브랜치별 시나리오로 데이터 분석을 실습할 수 있습니다.

### 추가 가이드

`00-system/03-guides/`에서 Claude Code 활용법을 더 깊이 배울 수 있습니다:

- **CLAUDE-MD-BEST-PRACTICES.md** - CLAUDE.md 작성 모범 사례
- **PROMPT-ENGINEERING-GUIDE.md** - 프롬프트 엔지니어링 가이드
- **TODO-SYSTEM-GUIDE.md** - Todo 시스템 활용법

---

## Tips

1. **setup-workspace 먼저**: `/setup-workspace`로 CLAUDE.md를 자동 생성하세요
2. **Inbox Zero**: `00-inbox/`는 정기적으로 비우세요
3. **Daily Habit**: 매일 Daily Note를 작성하세요
4. **Archive 활용**: 완료된 프로젝트는 `90-archive/`로 이동
5. **템플릿 커스터마이징**: 자신에게 맞게 템플릿을 수정하세요

## Why Johnny Decimal?

Johnny Decimal 시스템은:
- 명확한 카테고리 구조
- 쉬운 파일 찾기
- 확장 가능한 시스템
- AI가 이해하기 쉬운 구조

## Credits

Inspired by:
- [Claudesidian](https://github.com/heyitsnoah/claudesidian) by Noah Brier
- 15 years of F&B operations experience
- Real-world AI automation workflows

## License

MIT License - 자유롭게 사용하고 수정하세요!

## Support

Issues나 질문이 있으시면 GitHub Issues를 활용해주세요.

---

**Made with by hovoo (이림)**
F&B Professional × AI Practitioner
