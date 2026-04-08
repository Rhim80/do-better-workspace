# /todos - Todo List Viewer & Manager

저장된 모든 Todo를 다양한 방식으로 조회하고 관리하는 커맨드입니다.

## 사용법

```
/todos              # 전체 Todo 보기
/todos today        # 오늘 할 일만
/todos project      # 프로젝트별 그룹화
/todos overdue      # 1주일 이상 된 것들
/todos stats        # Todo 통계
```

## 작동 방식

### 1. `/todos` (기본 - 전체 보기)

`40-personal/46-todos/active-todos.md` 파일을 읽어서 표시

**출력 형식:**
```markdown
# 📋 전체 Todo 목록 (15개)

## 📥 Inbox (처리 안 한 것들) - 7개
- [ ] 클라이언트 제안서 마감
  - added: 2025-10-11 15:23
  - priority: high

- [ ] 프로젝트 문서 업데이트
  - added: 2025-10-11 16:45
  - priority: normal

## 🎯 Today (오늘 할 일) - 3개
...

## ⚠️ Overdue (1주일 이상) - 2개
...

---
💡 Tip: /todos today 로 오늘 할 일만 볼 수 있습니다.
```

### 2. `/todos today` (오늘 할 일)

**로직:**
1. active-todos.md 읽기
2. "🎯 Today" 섹션 추출
3. 우선순위별로 정렬 (high → normal → low)
4. 깔끔하게 표시

**출력 형식:**
```markdown
# 🎯 오늘 할 일 (3개)

## High Priority
- [ ] 클라이언트 제안서 마감 (15:23에 추가)

## Normal Priority
- [ ] 주간 보고서 작성 (12:30에 추가)
- [ ] 프로젝트 진행 체크리스트 작성 (10:15에 추가)

---
💡 완료하면 체크박스를 체크하고 저장하세요.
   자동으로 completed-todos.md로 아카이빙됩니다.
```

### 3. `/todos project` (프로젝트별)

**로직:**
1. active-todos.md의 모든 Todo 읽기
2. `project:` 필드로 그룹화
3. 프로젝트별로 표시

**출력 형식:**
```markdown
# 🗂️ 프로젝트별 Todo

## 📊 marketing-campaign (3개)
- [ ] 캠페인 성과 분석
- [ ] A/B 테스트 결과 정리
- [ ] 보고서 템플릿 업데이트

## 📋 client-project-a (4개)
- [ ] 요구사항 문서 검토
- [ ] 디자인 피드백 반영
- [ ] API 연동 테스트
- [ ] 배포 일정 확인

## 📚 online-course (2개)
- [ ] 커리큘럼 3주차 작성
- [ ] 실습 자료 준비

## 🔧 Unassigned (프로젝트 미지정) (1개)
- [ ] 외부 미팅 일정 조율

---
💡 /todo [프로젝트명] [내용] 으로 프로젝트 지정 가능
```

### 4. `/todos overdue` (오래된 것들)

**로직:**
1. 모든 Todo의 `added:` 필드 체크
2. 현재 시간 - 추가 시간 > 7일인 것 필터링
3. 오래된 순으로 정렬

**출력 형식:**
```markdown
# ⚠️ 오래된 Todo (1주일 이상)

## 🔴 14일 지남
- [ ] 서비스 이용약관 검토
  - added: 2025-09-27 10:30
  - project: client-project-a

## 🟠 10일 지남
- [ ] 월간 보고서 초안
  - added: 2025-10-01 14:20
  - project: 없음

---
⚠️ 장기 프로젝트는 괜찮지만, 급한 일이면 빠르게 처리하세요!
```

### 5. `/todos stats` (통계)

**로직:**
1. 전체 Todo 개수 집계
2. 우선순위별, 프로젝트별, 상태별 통계

**출력 형식:**
```markdown
# 📊 Todo 통계

## 전체 개요
- 총 Todo: 15개
- 완료율: 68% (이번 달 기준)
- 평균 완료 시간: 2.3일

## 우선순위별
- High: 3개 (20%)
- Normal: 10개 (67%)
- Low: 2개 (13%)

## 프로젝트별
- client-project-a: 5개
- marketing-campaign: 3개
- online-course: 2개
- 기타: 5개

## 상태별
- Inbox (미분류): 7개
- Today (오늘): 3개
- Scheduled (예정): 3개
- Overdue (지연): 2개

---
💡 /daily-review 실행 시 자동으로 Todo 제안이 포함됩니다.
```

## 추가 기능

### Auto-cleanup (자동 정리)
- 완료된 Todo (`[x]`)를 자동 감지
- `completed-todos.md`로 이동
- 월별로 아카이빙

### Smart Suggestions (똑똑한 제안)
```
💡 제안:
- "제안서 마감" - 2일 지남, 오늘 처리하시겠어요?
- "marketing" 관련 Todo 3개 - 한 번에 처리하면 효율적일 것 같아요
- 프로젝트 미지정 Todo 1개 - 프로젝트를 지정하시겠어요?
```

## 실행 흐름

1. 인자 파싱 (`today`, `project`, `overdue`, `stats`)
2. `active-todos.md` 파일 읽기
3. 인자에 따라 필터링/그룹화
4. 보기 좋게 포맷팅
5. 추가 제안 생성
6. 출력

**파일 경로:**
- 읽기: `40-personal/46-todos/active-todos.md`
- 아카이브: `pkm/40-personal/43-todos/completed-todos.md`
