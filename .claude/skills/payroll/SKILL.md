---
name: payroll
description: 한국 노동법/세무 기준 급여 관리 자동화. 회사 정보를 한 번 셋업하면 4대보험/소득세/일할계산/휴일가산/퇴직금까지 계산하고 세무사 전달용 Excel을 생성. "급여 처리", "급여대장 만들어", "퇴직금 계산", "payroll 셋업" 등 언급 시 자동 실행.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Skill
---

# Payroll Skill

한국 노동법/세무 기준 급여 관리 자동화. **회사별 정보를 한 번만 셋업**하면 매월 동일하게 동작.

> 글로벌 (이림 IMI 운영용) `~/.claude/skills/payroll/` 과는 독립.
> 이 워크스페이스 버전은 **범용 + 셋업 기반**이며, 부트캠프 참가자 누구나 자기 회사 정보로 바로 사용 가능.

---

## 1. 처음 셋업하기 (한 번만)

```bash
pip install openpyxl pyyaml google-api-python-client google-auth google-auth-oauthlib
python3 .claude/skills/payroll/scripts/setup.py --create-sheet
```

이걸로 끝입니다. 셋업 도구가 4단계로 묻고 (회사 정보 / 직원 규모 / 가산율 / 세무사),
**모르시는 항목은 그대로 Enter** 누르면 권장값으로 진행됩니다.
Google Sheets 직원DB도 자동으로 만들어지고, 시트 URL을 알려줍니다.

자세한 안내는 [payroll-setup-guide](../../../00-system/03-guides/payroll-setup-guide.md) 참고.

### 직원 정보만 직접 채워주세요
셋업이 끝나면 자동 생성된 Google Sheets `직원DB` 시트에 직원 정보를 입력하세요:

| 이름 | 주민번호 | 연락처 | 이메일 | 매장 | 직급 | 입사일 | 퇴사일 | 기본급 | 식대 | 부양가족 | 계좌 |
|------|----------|--------|--------|------|------|--------|--------|--------|------|----------|------|
| 홍길동 | 900101-1234567 | 010-... | a@b.c | 본점 | 매니저 | 2024-03-01 | | 2400000 | 200000 | 1 | ... |

---

## 2. 매월 급여 처리 (셋업 후)

### 호출 문구

| 요청 | 실행 내용 |
|------|-----------|
| **"이번 달 급여 처리하자"** | Step A부터 순차 진행 |
| **"급여변동.md 작성해줘"** | Step A 실행 |
| **"급여대장 생성해줘"** | Step B 실행 |
| **"세무사에게 급여대장 보내줘"** | Step C 실행 (발송 전 확인) |

### Step A. 급여변동.md 작성
> 휴일근무, 추가근무, 파트타이머, 일용직, 입퇴사 일할계산 등 월별 변동사항 정리

출력: `{output_base}/{year}/급여변동/YYYY-MM_급여변동.md`

기본 구조 (작성 가이드는 아래 [3. 급여변동.md 작성 가이드](#3-급여변동md-작성-가이드) 참고):
```markdown
# YYYY년 M월 급여 변동사항

## 1. 본점

### 정직원 - 휴일근무 수당
| 직원명 | 기본급 | 통상시급 | 휴일근무 | 가산율 | 수당 |
| ... |

### 파트타이머
| 직원명 | 주민번호 | 근무시간 | 시급 | 급여 | 비고 |
| ... |
```

### Step B. 급여대장 Excel 생성
```bash
# 미리보기 (파싱 결과 확인)
python3 .claude/skills/payroll/scripts/generate_payroll_excel.py 2026-01 --preview

# 실제 생성
python3 .claude/skills/payroll/scripts/generate_payroll_excel.py 2026-01
```

출력: `{output_base}/{year}/세무사자료/YYYY-MM_급여대장.xlsx`

**시트 구성**:
- 매장별 시트 (회사가 다중 사업장이면 매장마다 한 시트)
- 단일 사업장이면 회사명 한 시트
- `일용직` (전 매장 일용직, 실제 근무일 포함)
- `전체_합계` (사업장별/항목별 크로스체크용)

### Step C. 세무사 발송 (선택)
Gmail 스킬과 연동되어 있으면:
```bash
python3 ~/.claude/skills/gmail/scripts/gmail.py send \
  --to "{accountant_email}" \
  --subject "{year}년 {month}월 급여대장" \
  --body "..." \
  --attachment "{output_path}/YYYY-MM_급여대장.xlsx"
```

---

## 3. 급여변동.md 작성 가이드

### 섹션 종류

#### 정직원 - 휴일근무 수당
공휴일 스케줄 근무 (5인 미만이면 가산분만 0.5배)
```markdown
| 직원명 | 기본급 | 통상시급 | 휴일근무 | 가산율 | 수당 |
|--------|--------|----------|----------|--------|------|
| 홍길동 | 2,400,000원 | 11,483원 | 8시간 | 0.5배 | 45,933원 |
```

#### 정직원 - 추가근무 수당
다른 매장 지원 등 (5인 미만이면 1.0배)
```markdown
| 직원명 | 통상시급 | 추가근무 | 수당 |
| ... |
```

#### 정직원 - 일할계산 (신규/퇴사)
중도입사·퇴사
```markdown
| 항목 | 전액 | 일할계산 |
|------|------|----------|
| 입사일 | 2026-01-15 | |
| 근무일수 | 17일 (1/15~1/31) | |
| 기본급 | 2,050,000원 | 1,123,871원 |
| 식대 | 200,000원 | 109,677원 |
```

#### 파트타이머
```markdown
| 직원명 | 주민번호 | 근무시간 | 시급 | 급여 | 비고 |
| ... |
```

#### 일용직
**필수**: 실제 근무일(날짜) 포함 (고용/산재 근로내용확인신고용)
```markdown
| 직원명 | 주민번호 | 지급액 | 실제 근무일 | 근무일수 |
|--------|----------|--------|------------|----------|
| 박영희 | 850515-2345678 | 150,000원 | 2/3, 2/7, 2/14 | 3일 |
```

---

## 4. 계산 공식

> **중요**: 가산수당 비율은 회사·취업규칙·단체협약마다 다릅니다.
> 이 도구는 가산율을 자동 계산하지 않고, **사용자가 급여변동.md에 적은 수당 금액을 그대로 합산**합니다.
> 셋업 시 입력한 회사 가산율은 `company.yaml`의 `pay_rules`에 저장되어 가이드 역할만 합니다.

### 통상시급
```
통상시급 = 기본급 ÷ 209시간
```

### 가산수당 (회사 기준 따름)
```
가산수당 = 통상시급 × 회사 가산율 × 시간
```
회사 가산율의 한국 노동법 최저 기준은 `config/rates-kr-2026.yaml`의
`labor_law_minimum` 섹션 참고 (5인 이상은 연장 1.5배 등).
**5인 미만은 법정 의무 없음** — 회사가 자체로 정한 기준을 적용.

### 일할계산
```
일할급여 = (기본급 + 식대) × (근무일수 / 총일수)
```

### 주휴수당 (파트타이머, 주 5일 기준 예시)
```
주휴수당 = 기존급여 × 0.2
```
※ 회사·근무 형태에 따라 다를 수 있음. 실제 적용은 회계담당과 확인.

### 퇴직금
```
평균임금(일) = 최근 3개월 총 급여 / 3개월 총 일수
퇴직금 = max(평균임금, 통상임금) × 30 × (재직일수 / 365)
```
※ 최종 금액은 세무사 확정 기준 (퇴직소득세 별도).

---

## 5. 4대보험 공제 (2026년)

| 보험 | 근로자 부담 | 사업주 부담 |
|------|------------|------------|
| 국민연금 | 4.75% | 4.75% |
| 건강보험 | 3.595% | 3.595% |
| 장기요양 | 건보의 13.14% | 건보의 13.14% |
| 고용보험 | 0.9% | 0.9% (+ 규모별 추가) |
| 산재보험 | - | 업종별 (기본 0.7%) |
| 소득세 | 간이세액표 | - |
| 지방소득세 | 소득세의 10% | - |

요율 변경 시 `config/rates-kr-2026.yaml` 수정.

---

## 6. 두루누리 사회보험료 지원

신규입사자 입사 시 확인:
1. 월급여 270만원 미만?
2. 직전 1년간 4대보험 가입 이력 없음? (사회초년생, 경력단절 등)
3. 재산 6억 미만, 종합소득 4,300만 미만?

→ 해당 시 세무사에게 두루누리 신청 요청 (4대보험 80% 지원, 36개월)

---

## 7. 입퇴사자 처리

### 신규입사자
1. 직원DB에 정보 입력 (이름, 주민번호, 입사일, 매장, 기본급, 식대, 부양가족)
2. 세무사에 근로계약서 전달 → 4대보험 취득신고
3. 두루누리 지원 해당 여부 확인
4. 다음 달 급여변동.md에 일할계산 섹션 추가

### 퇴사자
1. 퇴사일 사전 공유 (4대보험 상실신고 - 최소 2주 전 권장)
2. 직원DB에 퇴사일 입력
3. 퇴직금 계산 (재직 1년 이상 시):
   ```bash
   python3 .claude/skills/payroll/scripts/retirement.py 홍길동 \
     --date 2026-02-28 --excel --save
   ```
4. **세무사 확정 급여로 검증** (Google Sheets 데이터와 차이 있을 수 있음):
   ```bash
   python3 .claude/skills/payroll/scripts/retirement.py 홍길동 \
     --date 2026-02-28 \
     --wages 2666667 2400000 2442105 \
     --excel --save --update-db
   ```

---

## 8. 스크립트 레퍼런스

| 스크립트 | 용도 |
|----------|------|
| `setup.py` | **셋업 (회사 정보 + Google Sheets 자동 생성)** |
| `payroll.py` | 급여 계산, 직원 조회 |
| `generate_payroll_excel.py` | **급여대장 Excel 생성** |
| `retirement.py` | **퇴직금 계산 + 퇴직금산정내역서 Excel** |
| `config_loader.py` | (내부) company.yaml + rates-kr-2026.yaml 통합 로드 |

### 자주 쓰는 명령
```bash
# 셋업/설정 확인
python3 setup.py
python3 setup.py --show
python3 setup.py --create-sheet

# 급여대장
python3 generate_payroll_excel.py 2026-01 --preview
python3 generate_payroll_excel.py 2026-01

# 직원 조회
python3 payroll.py employees
python3 payroll.py employees 본점

# 단순 급여 계산
python3 payroll.py calculate 2400000 --meal 200000 --dependents 2

# 퇴직금
python3 retirement.py 홍길동 --date 2026-02-28
python3 retirement.py 홍길동 --date 2026-02-28 \
  --wages 2666667 2400000 2442105 --excel --save
```

---

## 9. 설정 파일

| 파일 | 내용 | 공개 여부 |
|------|------|----------|
| `config/company.yaml` | 회사 정보, 매장, 세무사, Sheets ID | **.gitignore (비공개)** |
| `config/company.yaml.example` | 위 파일의 placeholder 템플릿 | 공개 (참고용) |
| `config/rates-kr-2026.yaml` | 한국 표준 4대보험 요율, 가산수당 | 공개 |
| `config/income_tax_table.json` | 국세청 간이세액표 334구간 | 공개 |

---

## 10. 산출물

| 파일 | 위치 | 용도 |
|------|------|------|
| 급여변동.md | `{output_base}/{year}/급여변동/YYYY-MM_급여변동.md` | 월별 변동사항 입력 |
| 급여대장.xlsx | `{output_base}/{year}/세무사자료/YYYY-MM_급여대장.xlsx` | 세무사 전달용 |
| 퇴직금산정내역서.xlsx | `{output_base}/{year}/세무사자료/{회사약칭} {이름} 퇴직금산정내역서.xlsx` | 퇴사자 퇴직금 산정 |
| 퇴직금계산.md | `{output_base}/{year}/입퇴사/YYYY-MM-DD_{이름}_퇴직금계산.md` | 기록용 |

`{output_base}`는 `company.yaml`의 `paths.output_base`로 설정.

---

## 11. 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `[setup 필요] company.yaml이 없습니다` | 셋업 미실행 | `python3 setup.py` 실행 |
| `Spreadsheet ID가 설정되지 않았습니다` | company.yaml의 `google_workspace.spreadsheet_id` 비어있음 | `setup.py --create-sheet`로 자동 생성하거나 직접 ID 입력 |
| `Google API 라이브러리가 없습니다` | google-api-python-client 미설치 | `pip install google-api-python-client google-auth google-auth-oauthlib` |
| 매장별 시트가 안 만들어짐 | `branches: []` (단일 사업장 모드) | 의도된 동작. 회사명 단일 시트로 출력됨 |
| 가산수당 금액이 회사 기준과 다름 | 급여변동.md에 적은 수당 금액이 회사 기준으로 계산되지 않았음 | 가산율 → company.yaml의 `pay_rules` 확인 → 급여변동.md의 "수당" 컬럼 직접 수정 |

---

## 관련 문서
- [payroll-setup-guide](../../../00-system/03-guides/payroll-setup-guide.md) - 단계별 셋업 가이드 (Google Sheets 직접 만드는 법, OAuth 등)

---

**최종 업데이트**: 2026-05-04
