---
description: 대화 내용에서 아이디어를 추출하고 PKM에 자동 저장
argument-hint: [카테고리: business/ai/operations/study/daily/random]
allowed-tools: Write, Read, Bash
---

우리가 방금 나눈 대화에서 아이디어나 인사이트를 추출하여 PKM 시스템에 저장해주세요.

**카테고리**: $ARGUMENTS (지정하지 않으면 자동 분류)

**수행할 작업:**
1. 대화 내용을 분석하여 핵심 아이디어 추출
2. 적절한 카테고리 판단 (business, ai, operations, study, daily, random 중 선택)
3. 해당 카테고리의 템플릿 사용하여 구조화된 문서 생성
4. `./30-knowledge/` 폴더에 날짜_제목.md 형식으로 저장 (폴더가 없으면 생성)
5. 저장된 파일 경로와 간단한 요약 제공

**중요사항:**
- 대화 맥락과 배경 정보 포함
- 실무 적용 가능성 고려
- 태그 추가로 나중에 검색 쉽게
- 후속 행동 제안 포함