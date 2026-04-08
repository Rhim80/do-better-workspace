---
name: csv-clean
description: CSV 데이터 품질 정리. 소계행 제거, 숫자 정리, 날짜 정규화, unpivot 등. "데이터 정리", "CSV 정리", "소계 제거", "숫자 정리", "날짜 통일", "unpivot", "csv clean", "데이터 클리닝" 등을 언급하면 자동 실행.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
---

# CSV Data Quality Cleaner

CSV 파일의 데이터 품질 문제를 정리한다. Excel 없이도 독립 사용 가능 (은행 CSV, API 내보내기 등).

## Script Location

`.claude/skills/csv-clean/scripts/csv-clean.py`

## Prerequisites

```bash
pip install pandas>=2.0.0
```

설치 여부를 먼저 확인하고, 없으면 설치한다.

## Workflow

### Step 1: CSV 파일 경로 확인

사용자로부터 CSV 파일 경로를 확인한다.
경로가 명확하지 않으면 Glob으로 .csv 파일을 스캔한다.

### Step 2: 데이터 품질 분석

```bash
python .claude/skills/csv-clean/scripts/csv-clean.py <파일경로> --info
```

출력 내용:
- 소계/합계 행 감지
- 텍스트 형식 숫자 감지
- 날짜 형식 불일치 감지
- 크로스탭 구조 감지

### Step 3: 감지 결과 해석 및 옵션 제안

분석 결과에 따라 적절한 옵션 조합을 사용자에게 제안한다:

| 감지 항목 | 제안 옵션 |
|----------|----------|
| SUBTOTAL_ROWS | `--remove-subtotals` |
| TEXT_NUMBERS | `--clean-numbers` 또는 `--clean-numbers-cols 열1,열2` |
| DATE_FORMATS | `--normalize-dates --date-cols 열명` |
| CROSSTAB | `--unpivot ID열1,ID열2` |

### Step 4: 정리 실행

```bash
# 소계 행 제거
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --remove-subtotals

# 숫자 정리 (자동 감지)
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --clean-numbers

# 특정 열만 숫자 정리
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --clean-numbers-cols 금액,단가

# 날짜 정규화
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --normalize-dates --date-cols 날짜

# 크로스탭 -> tidy data
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --unpivot 지역,제품

# 복합 옵션
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --remove-subtotals --clean-numbers --normalize-dates

# 출력 경로 지정
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --output /path/to/output.csv

# 원본 덮어쓰기
python .claude/skills/csv-clean/scripts/csv-clean.py <파일> --inplace
```

### Step 5: 결과 확인

정리 완료 후:
1. 변경 사항 요약 (행 수 변화, 정리된 값 수)
2. Read 도구로 첫 5행을 미리보기하여 품질 확인
3. 원본과 비교하여 의도하지 않은 변경이 없는지 확인

## Pipeline Usage

excel-to-csv와 연결하여 사용:

```bash
# Excel -> CSV -> 정리
python .claude/skills/excel-to-csv/scripts/excel-to-csv.py file.xlsx --all --flatten-headers
python .claude/skills/csv-clean/scripts/csv-clean.py file.csv --remove-subtotals --clean-numbers
```

## CLI Options

| 옵션 | 설명 |
|------|------|
| `--info` | 데이터 품질 분석만 (변환 안 함) |
| `--remove-subtotals` | 소계/합계 행 제거 |
| `--clean-numbers` | 숫자 정리 (자동 감지) |
| `--clean-numbers-cols COLS` | 특정 열만 숫자 정리 |
| `--normalize-dates` | 날짜 형식 통일 |
| `--date-format FMT` | 날짜 출력 형식 (기본: %Y-%m-%d) |
| `--date-cols COLS` | 날짜 대상 열 지정 |
| `--unpivot ID_COLS` | 크로스탭 unpivot |
| `--value-name NAME` | unpivot 값 열 이름 |
| `--variable-name NAME` | unpivot 변수 열 이름 |
| `--normalize-text COL=MAPFILE` | 텍스트 표현 통일 |
| `--output PATH` | 출력 파일 경로 |
| `--inplace` | 원본 덮어쓰기 |

## Output Naming

| 조건 | 파일명 패턴 |
|------|------------|
| 기본 | `{원본파일명}_cleaned.csv` |
| `--output` 지정 | 지정된 경로 |
| `--inplace` | 원본 파일 덮어쓰기 |

## Error Handling

- `pandas` 미설치 시: `pip install pandas>=2.0.0` 실행 안내
- 파일 못 찾음: 경로 확인 안내
- 열 이름 오류: 사용 가능한 열 목록 표시
