---
description: 오늘 날짜의 Daily Note 생성 또는 열기
allowed-tools: Read, Write, Edit, Bash
---

오늘 날짜의 Daily Note를 생성하거나 열어주세요.

**수행할 작업:**

1. 오늘 날짜 확인 (YYYY-MM-DD 형식)
2. 경로 (월별 하위 폴더 구조):
   - 폴더: `./40-personal/41-daily/YYYY-MM/`
   - 파일: `./40-personal/41-daily/YYYY-MM/YYYY-MM-DD.md`
   - 월별 폴더가 없으면 자동 생성
3. 파일이 없으면:
   - 템플릿 읽기:
     - `./00-system/01-templates/daily-note-template.md`
   - 변수 치환:
     - `{{date}}`: 오늘 날짜 (예: 2026-04-08)
     - `{{weekday}}`: 오늘 요일 (예: 화요일)
     - `{{yesterday}}`: 어제 날짜
     - `{{tomorrow}}`: 내일 날짜
     - `{{week}}`: 이번 주차 (예: 2026-W15)
   - 새 파일 생성
4. 파일이 있으면:
   - 현재 내용 표시
