---
name: notion-handler
description: Notion 데이터베이스/페이지 관리. "노션", "Notion", "DB 만들어", "데이터베이스", "페이지 추가", "설문 DB", "프로젝트 관리", "노션에 저장", "대시보드" 등을 언급하면 자동 실행.
allowed-tools: Bash, Read, Write
---

# Notion Handler Skill

## Prerequisites

### Required: NOTION_TOKEN 환경변수

토큰이 설정되어 있어야 합니다:
```bash
export NOTION_TOKEN="your_notion_token_here"
```

---

## 주요 기능

### 1. 데이터베이스 (Database)

#### DB 생성
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py create-db \
  --parent "페이지ID" \
  --title "DB 제목" \
  --properties '{"이름": "title", "회사": "rich_text", "상태": {"select": ["진행중", "완료"]}}'
```

#### DB 조회
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py query-db \
  --id "DB_ID" \
  --filter '{"property": "상태", "select": {"equals": "완료"}}'
```

#### DB 정보 확인
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py get-db --id "DB_ID"
```

---

### 2. 페이지 (Page)

#### 페이지 생성 (DB 항목)
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py create-page \
  --parent "DB_ID" \
  --properties '{"이름": "홍길동", "회사": "ABC Corp"}'
```

#### 페이지 조회
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py get-page --id "PAGE_ID"
```

#### 페이지 수정
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py update-page \
  --id "PAGE_ID" \
  --properties '{"상태": "완료"}'
```

---

### 3. 블록 (Block)

#### 블록 추가
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py append-blocks \
  --id "PAGE_ID" \
  --blocks '[{"type": "heading_2", "text": "섹션 제목"}, {"type": "paragraph", "text": "내용"}]'
```

#### 지원 블록 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| `heading_1` | 제목 1 | `{"type": "heading_1", "text": "제목"}` |
| `heading_2` | 제목 2 | `{"type": "heading_2", "text": "부제목"}` |
| `heading_3` | 제목 3 | `{"type": "heading_3", "text": "섹션"}` |
| `paragraph` | 본문 | `{"type": "paragraph", "text": "내용"}` |
| `bulleted_list_item` | 글머리 기호 | `{"type": "bulleted_list_item", "text": "항목"}` |
| `numbered_list_item` | 번호 목록 | `{"type": "numbered_list_item", "text": "항목"}` |
| `to_do` | 체크박스 | `{"type": "to_do", "text": "할 일", "checked": false}` |
| `divider` | 구분선 | `{"type": "divider"}` |
| `image` | 외부 이미지 | `{"type": "image", "url": "https://..."}` |
| `bookmark` | 북마크 링크 | `{"type": "bookmark", "url": "https://..."}` |
| `quote` | 인용문 | `{"type": "quote", "text": "인용 내용"}` |
| `callout` | 콜아웃 | `{"type": "callout", "text": "내용", "emoji": "💡"}` |
| `code` | 코드 블록 | `{"type": "code", "text": "코드", "language": "python"}` |
| `toggle` | 토글 | `{"type": "toggle", "text": "토글 제목"}` |

#### 블록 조회 (기본)
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py get-blocks --id "PAGE_ID"
```

#### 블록 조회 (페이지네이션 포함)
```bash
# 모든 블록 가져오기
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py get-all-blocks --id "PAGE_ID"

# 중첩 블록까지 재귀적으로 가져오기
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py get-all-blocks --id "PAGE_ID" --recursive
```

#### 블록 수정
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py update-block \
  --id "BLOCK_ID" \
  --content '{"paragraph": {"rich_text": [{"text": {"content": "수정된 내용"}}]}}'
```

#### 블록 삭제
```bash
# 단일 블록 삭제
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py delete-block --id "BLOCK_ID"

# 여러 블록 삭제
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py delete-blocks \
  --ids '["BLOCK_ID_1", "BLOCK_ID_2", "BLOCK_ID_3"]'

# 페이지 전체 블록 삭제 (페이지 초기화)
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py clear-page --id "PAGE_ID"
```

---

### 4. 검색

```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py search --query "검색어"

# 페이지만 검색
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py search --query "검색어" --type page

# 데이터베이스만 검색
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py search --query "검색어" --type database
```

---

## 속성 타입 참조

| 타입 | 설명 | 예시 |
|------|------|------|
| `title` | 제목 (필수) | `"이름": "title"` |
| `rich_text` | 텍스트 | `"설명": "rich_text"` |
| `number` | 숫자 | `"연차": "number"` |
| `select` | 단일 선택 | `"상태": {"select": ["진행중", "완료"]}` |
| `multi_select` | 다중 선택 | `"태그": {"multi_select": ["A", "B"]}` |
| `checkbox` | 체크박스 | `"완료": "checkbox"` |
| `date` | 날짜 | `"마감일": "date"` |
| `email` | 이메일 | `"이메일": "email"` |
| `phone_number` | 전화번호 | `"연락처": "phone_number"` |
| `url` | URL | `"링크": "url"` |

---

## 사용 예시

### 설문 DB 생성
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py create-db \
  --parent "2bbd0f53623d80b49e3ed311fe1f6038" \
  --title "HFK Winter 2025 사전 설문" \
  --properties '{
    "이름": "title",
    "회사": "rich_text",
    "직무": "rich_text",
    "연차": "number",
    "AI 도구 경험": {"multi_select": ["ChatGPT", "Claude", "Copilot", "Gemini", "기타"]},
    "AI 활용 수준": {"select": ["입문", "초급", "중급", "고급"]},
    "기대 사항": "rich_text",
    "현재 업무 고충": "rich_text",
    "노트북 지참": "checkbox",
    "제출일": "date"
  }'
```

### 설문 응답 추가
```bash
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py create-page \
  --parent "DB_ID" \
  --properties '{
    "이름": "권오훈",
    "회사": "노동법률사무소 유록",
    "직무": "공인노무사",
    "연차": 7,
    "AI 도구 경험": ["ChatGPT"],
    "AI 활용 수준": "초급",
    "노트북 지참": true
  }'
```

### 아티클 번역 및 이미지 포함 페이지 생성
```bash
# 1. 페이지 초기화 (기존 블록 삭제)
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py clear-page --id "PAGE_ID"

# 2. 콘텐츠 추가 (이미지, 북마크, 콜아웃 포함)
python3 ~/.claude/skills/notion-handler/scripts/notion_api.py append-blocks \
  --id "PAGE_ID" \
  --blocks '[
    {"type": "heading_1", "text": "아티클 제목"},
    {"type": "callout", "text": "핵심 요약 내용", "emoji": "💡"},
    {"type": "paragraph", "text": "본문 내용..."},
    {"type": "image", "url": "https://example.com/image.jpg"},
    {"type": "heading_2", "text": "섹션 제목"},
    {"type": "bulleted_list_item", "text": "항목 1"},
    {"type": "bulleted_list_item", "text": "항목 2"},
    {"type": "quote", "text": "인용문"},
    {"type": "code", "text": "const x = 1;", "language": "javascript"},
    {"type": "divider"},
    {"type": "bookmark", "url": "https://example.com/source"}
  ]'
```

---

## CLI 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `create-db` | 데이터베이스 생성 |
| `get-db` | 데이터베이스 정보 조회 |
| `query-db` | 데이터베이스 쿼리 |
| `update-db` | 데이터베이스 수정 |
| `create-page` | 페이지 생성 |
| `get-page` | 페이지 정보 조회 |
| `update-page` | 페이지 수정 |
| `archive-page` | 페이지 삭제 (아카이브) |
| `append-blocks` | 블록 추가 |
| `get-blocks` | 블록 조회 |
| `get-all-blocks` | 블록 전체 조회 (페이지네이션) |
| `update-block` | 블록 수정 |
| `delete-block` | 블록 삭제 |
| `delete-blocks` | 여러 블록 삭제 |
| `clear-page` | 페이지 초기화 |
| `search` | 검색 |

---

## 보안

- `NOTION_TOKEN`은 환경변수로 관리
- 토큰을 코드나 문서에 하드코딩 금지

---

## Version History

- **v1.1.0 (2026-01-03)**: 블록 타입 확장 (image, bookmark, quote, callout, code, toggle), 블록 관리 기능 추가 (delete-block, delete-blocks, clear-page, get-all-blocks, update-block)
- **v1.0.0 (2025-11-30)**: 초기 작성 - DB/페이지/블록/검색 지원
