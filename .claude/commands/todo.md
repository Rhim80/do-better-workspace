# /todo - Quick Todo Capture

빠르게 Todo를 추가하는 커맨드입니다.

## 사용법

```
/todo 프로젝트 보고서 초안 작성
/todo [urgent] 클라이언트 미팅 자료 준비
/todo [my-project] 리서치 결과 정리
```

## 작동 방식

1. **컨텍스트 자동 수집**
   - 현재 작업 중인 파일 경로
   - 추가 시각 (timestamp)
   - 현재 프로젝트 디렉토리

2. **우선순위 자동 감지**
   - `[urgent]` 또는 `[high]` → high priority
   - `[low]` → low priority
   - 없으면 → normal priority

3. **프로젝트 자동 연결**
   - `[프로젝트명]` → 해당 프로젝트에 연결
   - 현재 디렉토리가 프로젝트면 자동 연결

4. **저장 위치**
   - `40-personal/46-todos/active-todos.md`의 "📥 Inbox" 섹션

## 실행

사용자가 제공한 Todo 내용을 다음 형식으로 저장:

```markdown
- [ ] [Todo 내용]
  - added: YYYY-MM-DD HH:mm
  - context: [현재 작업 파일 경로]
  - priority: [high/normal/low]
  - project: [프로젝트명 (있으면)]
```

**단계:**
1. 현재 git 디렉토리 확인 (`pwd`)
2. Todo 내용 파싱 (우선순위, 프로젝트 태그 추출)
3. active-todos.md 읽기
4. "📥 Inbox" 섹션에 새 항목 추가
5. 파일 저장
6. 확인 메시지 출력: "✅ Todo 추가됨: [내용]"

**컨텍스트 보존:**
- 사용자가 현재 어떤 작업 중인지 추적
- 나중에 "/todos project" 실행 시 프로젝트별로 그룹화 가능

**예시 출력:**
```
✅ Todo 추가됨: 프로젝트 보고서 초안 작성
   Priority: normal
   Context: my-project/README.md

   📝 /todos 로 전체 목록을 확인하세요.
```
