# IMI Workspace

> AI-powered workspace for non-coders
> 비개발자를 위한 AI 작업 환경

---

## What is IMI Workspace?

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
git clone https://github.com/Rhim80/imi-workspace.git
cd imi-workspace
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
| `/gather` | 정보 수집 모드 |
| `/reframe` | 이해 확인 모드 |
| `/truth` | 사실 기반 분석 모드 |
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
imi-workspace/
├── 00-inbox/          # 빠른 캡처 공간
├── 00-system/         # 시스템 설정 및 템플릿
│   ├── 01-templates/
│   ├── 02-scripts/
│   └── 03-guides/
├── 10-projects/       # 활성 프로젝트 (시한부)
│   └── 11-consulting/ # 컨설팅 프레임워크
├── 20-operations/     # 비즈니스 운영 (지속적)
│   └── 21-hr/         # HR/노무 관련
├── 30-knowledge/      # 지식 아카이브
├── 40-personal/       # 개인 노트
│   ├── 41-daily/      # Daily Notes
│   ├── 42-weekly/     # Weekly Reviews
│   └── 46-todos/      # 할 일 관리
├── 50-resources/      # 참고 자료
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
- `01-templates/` - 재사용 가능한 템플릿
- `02-scripts/` - 자동화 스크립트
- `03-guides/` - 가이드 문서

**수정 가능**: 필요에 따라 템플릿 커스터마이징

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
│   ├── 입사신고-template.md
│   └── 퇴사신고-template.md
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
├── 31-business-frameworks/
│   ├── lean-canvas.md
│   └── okr-system.md
├── 32-technical-guides/
└── 33-industry-insights/
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
│   └── 2025-12/
│       ├── 2025-12-28.md
│       └── 2025-12-29.md
├── 42-weekly/
│   ├── 2025-W52.md
│   └── 2025-W53.md
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
├── 2024-Q4/
│   ├── 11-website-redesign/
│   └── 12-product-launch/
└── 2025-Q1/
```

## Templates

`00-system/01-templates/`에서 사용 가능한 템플릿:

- **daily-note-template.md** - 매일 작성하는 노트
- **weekly-review-template.md** - 주간 회고
- **Project Template.md** - 새 프로젝트 시작

## Slash Commands

`.claude/commands/`에서 사용 가능한 커맨드:

### 초기 설정
- `/setup-workspace` - **대화형 CLAUDE.md 자동 생성** + 초기 설정
- `/setup-google-calendar` - Google Calendar 통합 설정

### Daily Workflow
- `/daily-note` - 오늘 날짜의 Daily Note 생성/열기
- `/daily-review` - 어제와 오늘 변경사항 분석
- `/todo` / `/todos` - 할 일 관리

### Thinking & Ideas
- `/thinking-partner` - 생각 정리 파트너 (소크라테스식 질문)
- `/idea` - 대화에서 아이디어 추출 및 저장

### Orchestration Commands
- `/gather` - 정보 수집 모드 (구조화된 질문 생성)
- `/reframe` - 이해 확인 모드 (대화 요약 및 확인)
- `/truth` - 사실 기반 분석 모드 (객관적 분석)

### 시스템
- `/create-command` - 커스텀 명령어 생성

> **프로젝트 스킬 (`.claude/skills/`)**: 이 워크스페이스에만 적용되는 skills로, 전역 스킬(`~/.claude/skills/`)과 독립적으로 작동합니다.

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

`50-resources/sample-data/`에 **교육용 샘플 데이터**가 포함되어 있습니다.

### 오피스원 주식회사 시나리오

가상의 B2B 사무용품 회사 **오피스원 주식회사**의 데이터로 실습합니다:

| 데이터 | 설명 | 레코드 수 |
|--------|------|-----------|
| `sample_sales_data.csv` | 2분기 판매 실적 | 117건 |
| `customer_data.csv` | 고객사 정보 | 50개사 |
| `employee_survey_data.csv` | 직원 만족도 설문 | 50명 |
| `inventory_data.csv` | 재고 현황 | 40품목 |
| `marketing_campaign_data.csv` | 마케팅 캠페인 | 24건 |

### 실습 가이드

`00-system/claude-code-practice-guide.md`에서 6가지 미션을 통해 데이터 분석을 배울 수 있습니다:

1. **판매 실적 분석** - 월별/지역별/담당자별 매출 분석
2. **고객 현황 점검** - VIP 고객 식별, 이탈 패턴 분석
3. **마케팅 ROI 검토** - 채널별 효율성 비교
4. **재고 관리 이슈** - 긴급 발주 품목 식별
5. **직원 만족도 분석** - 부서별 비교, 개선점 도출
6. **종합 보고서** - CEO 보고용 1페이지 요약

> **스토리**: 당신은 경영기획팀 신입 사원입니다. 2분기 말 경영 회의를 앞두고 박 팀장이 데이터 분석을 요청합니다.

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
