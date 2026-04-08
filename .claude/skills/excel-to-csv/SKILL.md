---
name: excel-to-csv
description: Excel 파일을 CSV로 변환하여 Claude Code에서 분석 가능하게 만듦. "엑셀 변환", "Excel CSV", "xlsx 변환", "엑셀을 CSV로", "데이터 변환", "excel to csv" 등을 언급하거나 .xlsx/.xls 파일 경로를 제공하면 자동 실행.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Skill
---

# Excel to CSV Converter

Claude Code는 .xlsx/.xls 파일을 직접 읽을 수 없다. 이 스킬은 Excel 파일을 UTF-8 CSV로 변환하여 분석 가능하게 만든다.

## Script Location

`.claude/skills/excel-to-csv/scripts/excel-to-csv.py`

## Prerequisites

```bash
pip install openpyxl>=3.1.0
```

설치 여부를 먼저 확인하고, 없으면 설치한다.

## Workflow

### Step 1: 파일 경로 확인

사용자로부터 Excel 파일 경로 또는 폴더 경로를 확인한다.
경로가 명확하지 않으면 Glob으로 .xlsx/.xls 파일을 스캔한다.

### Step 2: 파일 정보 분석

```bash
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --info
```

출력 내용:
- 시트 목록
- 각 시트의 행/열 수
- 헤더 미리보기
- 데이터 미리보기 (첫 3행)
- **Complexity Analysis**: 구조 문제 자동 감지

### Step 2.5: 복잡성 분석 결과 해석

`--info` 출력의 Complexity Analysis 섹션을 확인한다:

| 감지 항목 | 의미 | 해결 방법 |
|----------|------|----------|
| MULTI_HEADER | 다단 헤더 | `--flatten-headers` 옵션 사용 |
| METADATA_SKIP | 메타데이터 행 | `--skip-rows N` 옵션 사용 |
| SUBTOTAL_ROWS | 소계/합계 행 | 변환 후 `csv-clean --remove-subtotals` |
| TEXT_NUMBERS | 서식 있는 숫자 | 변환 후 `csv-clean --clean-numbers` |
| CROSSTAB | 크로스탭 구조 | 변환 후 `csv-clean --unpivot` |
| DATE_FORMATS | 날짜 혼재 | 변환 후 `csv-clean --normalize-dates` |

Excel 구조 문제는 이 스킬의 옵션으로 해결하고, 데이터 품질 문제는 "변환 후 csv-clean으로 정리하겠습니다"라고 안내한다.

### Step 3: CSV 변환 실행

```bash
# 기본 변환
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --all

# 특정 시트만
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --sheet "시트명"

# 다단 헤더 평탄화
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --all --flatten-headers

# 메타데이터 건너뛰기 + 헤더 평탄화
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --all --skip-rows 3 --flatten-headers

# 헤더 행 수 수동 지정
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --all --flatten-headers --header-rows 2

# 출력 경로 지정
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <파일경로> --all --output /path/to/output/

# 폴더 일괄 변환
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <폴더경로> --all

# CSV 인코딩 변환 (EUC-KR -> UTF-8)
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py <csv파일경로> --encoding euc-kr
```

### Step 4: 결과 확인

변환 완료 후:
1. 생성된 CSV 파일 목록과 행 수를 표시한다
2. Read 도구로 첫 5행을 미리보기하여 변환 품질을 확인한다
3. 한글이 깨지지 않았는지 확인한다

### Step 5: 데이터 정리 (필요 시)

Complexity Analysis에서 데이터 품질 문제가 감지된 경우, `/csv-clean` 스킬을 Skill tool로 호출하거나 직접 스크립트를 실행한다:

```bash
# 소계 제거 + 숫자 정리
python .claude/skills/csv-clean/scripts/csv-clean.py <변환된csv> --remove-subtotals --clean-numbers

# 날짜 정규화
python .claude/skills/csv-clean/scripts/csv-clean.py <변환된csv> --normalize-dates
```

## CLI Options

| 옵션 | 설명 |
|------|------|
| `--info` | 시트 정보 + 복잡성 분석 |
| `--sheet <name>` | 특정 시트만 변환 |
| `--output <path>` | 출력 디렉토리 |
| `--all` | 전체 시트 변환 |
| `--encoding <enc>` | CSV 인코딩 강제 지정 |
| `--flatten-headers` | 다단 헤더를 "상위_하위" 형태로 평탄화 |
| `--header-rows N` | 헤더 행 수 수동 지정 (기본: 자동감지) |
| `--skip-rows N` | 상단 N행 건너뛰기 (메타데이터) |

## Output Naming Rules

| 조건 | 파일명 패턴 |
|------|------------|
| 단일 시트 Excel | `{원본파일명}.csv` |
| 멀티 시트 Excel | `{원본파일명}_{시트명}.csv` |
| CSV 인코딩 변환 | `{원본파일명}_utf8.csv` |

- 공백 -> 언더스코어로 치환
- 특수문자 제거
- 한글 파일명 유지

## Supported Formats

| 입력 | 처리 방식 |
|------|----------|
| .xlsx | openpyxl로 읽음 (인코딩 이슈 없음) |
| .xls | openpyxl 호환 시 처리, 아니면 안내 |
| .csv | 인코딩 변환만 수행 (EUC-KR/CP949 -> UTF-8) |

## Data Handling

- 헤더 행: 첫 번째 비어있지 않은 행을 자동 감지
- 빈 행/열: 후행 빈 행과 열 자동 제거
- 병합 셀: 첫 번째 셀 값으로 채움
- 다단 헤더: `--flatten-headers`로 "상위_하위" 결합
- 메타데이터: `--skip-rows`로 건너뛰기
- 출력 인코딩: 항상 UTF-8

## Error Handling

- `openpyxl` 미설치 시: `pip install openpyxl>=3.1.0` 실행 안내
- 파일 못 찾음: 경로 확인 안내
- 시트 이름 오류: 사용 가능한 시트 목록 표시
- 인코딩 문제: `--encoding` 옵션으로 강제 지정 안내
