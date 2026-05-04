#!/usr/bin/env python3
"""
Payroll 셋업 - 초보자 친화 대화형

원칙:
  - 사용자가 답할 수 있는 질문만 한다 (한국 노동법 용어 X)
  - 기본값은 권장값으로 미리 채우고 그대로 Enter만 눌러도 동작하게
  - 어려운 단계는 모두 "지금은 건너뜀, 나중에 가능" 옵션 제공
  - Spreadsheet URL을 붙여넣으면 ID 자동 추출

Usage:
    python3 setup.py                    # 대화형 (권장)
    python3 setup.py --show             # 현재 설정 확인
    python3 setup.py --create-sheet     # company.yaml + Google Sheets 직원DB 자동 생성
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
import yaml

CONFIG_DIR = Path(__file__).parent.parent / 'config'
COMPANY_PATH = CONFIG_DIR / 'company.yaml'
EXAMPLE_PATH = CONFIG_DIR / 'company.yaml.example'

EMPLOYEE_DB_HEADERS = [
    '이름', '주민번호', '연락처', '이메일',
    '매장', '직급', '입사일', '퇴사일',
    '기본급', '식대', '부양가족', '계좌',
]


def ask(prompt: str, default: str = '', required: bool = False, hint: str = '') -> str:
    """질문하기. default가 있으면 [그대로 Enter: 기본값] 표시. hint는 한 줄 부연."""
    if hint:
        print(f"    ({hint})")
    suffix = f" [기본값 {default}]" if default else ''
    while True:
        value = input(f"  > {prompt}{suffix}: ").strip()
        if not value:
            value = default
        if required and not value:
            print("    ※ 빈 채로 둘 수 없어요. 다시 입력해주세요.")
            continue
        return value


def ask_yes(prompt: str, default_yes: bool = True, hint: str = '') -> bool:
    """예/아니오. 기본값을 쉽게 표시."""
    if hint:
        print(f"    ({hint})")
    default = "Y/n" if default_yes else "y/N"
    while True:
        v = input(f"  > {prompt} [{default}]: ").strip().lower()
        if not v:
            return default_yes
        if v in ("y", "yes", "ㅛ"):
            return True
        if v in ("n", "no", "ㅜ"):
            return False
        print("    ※ y 또는 n 으로 답해주세요.")


def extract_spreadsheet_id(text: str) -> str:
    """URL을 붙여넣으면 ID만 추출. ID를 그대로 넣어도 OK."""
    text = text.strip()
    if not text:
        return ""
    m = re.search(r'/spreadsheets/d/([a-zA-Z0-9_-]+)', text)
    if m:
        return m.group(1)
    if re.fullmatch(r'[a-zA-Z0-9_-]{20,}', text):
        return text
    return text


def build_config() -> dict:
    """초보자 친화 대화형. 한국 노동법 용어 안 쓰고 회사 정보만 묻는다."""
    print()
    print("=" * 60)
    print("  Payroll 셋업 — 회사 정보를 한 번만 입력합니다")
    print("=" * 60)
    print("  ※ 모든 질문은 그대로 Enter만 눌러도 권장값으로 진행됩니다.")
    print("  ※ 나중에 config/company.yaml 파일을 직접 수정해도 됩니다.")
    print()

    # ── 회사 ────────────────────────────────────────
    print("[1/4] 회사 기본 정보")
    name = ask("회사 이름이 뭔가요?", required=True,
               hint="예: A카페, 주식회사 OO")
    business_owner = ask("사업주(대표) 성함이 뭔가요?", required=True,
                          hint="퇴직금 서류에 들어갑니다")
    short_name = ask("회사를 짧게 부를 때 어떻게 표시할까요?",
                     default=name,
                     hint="퇴직금 서류 파일명에 쓰입니다. 회사명 그대로면 Enter")

    # ── 직원 수 → 5인 미만 자동 ────────────────────
    print()
    print("[2/4] 직원 규모와 매장")
    emp_count_raw = ask("총 직원이 몇 명이나 되나요? (사장 제외)",
                         default="5",
                         hint="정확하지 않아도 OK. 5명 미만/이상만 구분합니다")
    try:
        emp_count = int(re.sub(r'[^\d]', '', emp_count_raw) or "5")
    except ValueError:
        emp_count = 5
    under5 = emp_count < 5
    print(f"    → '{emp_count}명' 으로 인식 → "
          + ("5인 미만 사업장으로 처리합니다." if under5
             else "5인 이상 사업장으로 처리합니다."))

    # ── 매장 ────────────────────────────────────
    print()
    has_branches = ask_yes("매장(사업장)이 여러 개인가요?",
                            default_yes=False,
                            hint="단일 매장/사무실이면 N")
    branches = []
    branch_prefix = {}
    if has_branches:
        raw = ask("매장 이름들을 쉼표로 구분해서 적어주세요",
                  required=True,
                  hint="예: 본점, 강남점, 홍대점")
        branches = [b.strip() for b in raw.split(',') if b.strip()]
        long_branches = [b for b in branches if len(b) > 4]
        if long_branches:
            use_short = ask_yes(
                "매장 이름이 좀 길어요. Excel 시트 탭에서는 짧게 줄일까요?",
                default_yes=True,
                hint="예: '강남2호점' → '강남2'",
            )
            if use_short:
                for b in branches:
                    short = ask(f"'{b}' 줄임말", default=b[:3])
                    branch_prefix[b] = short

    # ── 가산수당 (자동 권장값 + 모르면 그대로) ────────
    print()
    print("[3/4] 휴일·추가근무 수당 (모르시면 그대로 Enter)")
    print("    ※ 회사가 직원에게 휴일 또는 추가 근무 시간에 대해")
    print("      얼마를 더 주는지 회사 규칙에 따라 다릅니다.")
    print("    ※ 잘 모르겠으면 한국 일반 회사 기본값으로 두고,")
    print("      나중에 회계담당/세무사에게 물어서 수정해도 됩니다.")
    if under5:
        ot_default = "1.0"
        hol_default = "1.0"
        print(f"    → 5인 미만 사업장: 법적 의무는 없어 기본값 1.0 (가산 없음)")
    else:
        ot_default = "1.5"
        hol_default = "1.5"
        print(f"    → 5인 이상 사업장: 법정 최저 1.5배가 기본값")

    overtime_rate = _safe_float(ask("추가/연장 근무 시 시급의 몇 배를 주나요?",
                                     default=ot_default,
                                     hint="1.0=가산 없음, 1.5=50% 더 줌"),
                                 fallback=float(ot_default))
    holiday_rate = _safe_float(ask("휴일 근무 시 시급의 몇 배를 주나요?",
                                    default=hol_default),
                                fallback=float(hol_default))
    night_rate = _safe_float(ask("야간(22~06시) 추가 가산율 (안 주면 0)",
                                  default="0.5"),
                              fallback=0.5)

    # ── 세무사 (선택) ────────────────────────────
    print()
    print("[4/4] 세무사 정보 (선택)")
    has_acc = ask_yes("세무사에게 이 도구로 메일도 보내실 건가요?",
                       default_yes=False,
                       hint="N으로 답하면 세무사 입력은 통째 건너뜁니다")
    if has_acc:
        acc_name = ask("세무사 성함", required=True)
        acc_email = ask("세무사 이메일", required=True)
        acc_company = ask("세무회계법인명", default="")
    else:
        acc_name = acc_email = acc_company = ""

    # ── Google Sheets (URL/ID, 비워도 OK) ────────────
    print()
    has_sheet = ask_yes("이미 만들어둔 Google Sheets 직원DB가 있나요?",
                         default_yes=False,
                         hint="없으면 N → 셋업 후 --create-sheet 옵션으로 자동 생성 가능")
    spreadsheet_id = ""
    if has_sheet:
        raw = ask("그 시트의 URL 또는 ID를 붙여넣어 주세요",
                  required=True,
                  hint="브라우저 주소창의 docs.google.com/spreadsheets/d/... 부분")
        spreadsheet_id = extract_spreadsheet_id(raw)
        if spreadsheet_id != raw:
            print(f"    → ID 추출 완료: {spreadsheet_id}")

    # ── cfg 조립 ────────────────────────────────
    cfg = {
        'company': {
            'name': name,
            'short_name': short_name,
            'business_owner': business_owner,
            'industry_code': '기타',
            'employee_count_estimate': emp_count,
            'under_5_employees': under5,
            'branches': branches,
            'branch_prefix': branch_prefix,
        },
        'pay_rules': {
            'overtime_rate': overtime_rate,
            'holiday_rate': holiday_rate,
            'holiday_bonus_only_rate': None,
            'night_extra_rate': night_rate,
            'notes': (
                f"셋업 시 입력값. 5인 {'미만' if under5 else '이상'} 사업장 기준. "
                "회사 단체협약/취업규칙으로 다를 수 있으니 회계담당과 확인하세요."
            ),
        },
        'accountant': {
            'email': acc_email,
            'name': acc_name,
            'company': acc_company,
        },
        'sender': {
            'name': name,
            'signature': f"감사합니다.\n\n{name} 드림\n",
        },
        'mail_templates': {
            'monthly_payroll': {
                'subject': '{year}년 {month}월 급여대장',
                'body': (
                    "안녕하세요,\n\n"
                    "{month}월 급여대장 전달드립니다.\n"
                    "확인 부탁드립니다.\n\n"
                    "감사합니다.\n"
                    f"{name} 드림\n"
                ),
            },
        },
        'google_workspace': {
            'spreadsheet_id': spreadsheet_id,
            'sheets': {
                'employees': '직원DB',
                'payroll_prefix': '_급여대장',
            },
        },
        'paths': {
            'output_base': '20-operations/payroll',
            'excel_folder': '{year}/세무사자료',
            'payroll_record': '{year}/급여변동',
            'resignation_folder': '{year}/입퇴사',
        },
        'metadata': {
            'setup_date': datetime.now().isoformat(timespec='seconds'),
            'config_version': '1.1',
        },
    }
    return cfg


def _safe_float(s: str, fallback: float) -> float:
    try:
        return float(s)
    except (ValueError, TypeError):
        return fallback


def write_config(cfg: dict):
    if COMPANY_PATH.exists():
        backup = COMPANY_PATH.with_suffix(
            f'.yaml.backup-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
        )
        COMPANY_PATH.rename(backup)
        print(f"\n  기존 company.yaml 백업: {backup.name}")

    with open(COMPANY_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(cfg, f, allow_unicode=True, sort_keys=False, width=80)

    print(f"  저장됨: {COMPANY_PATH.relative_to(Path.cwd())}"
          if COMPANY_PATH.is_relative_to(Path.cwd())
          else f"  저장됨: {COMPANY_PATH}")


def create_employee_sheet(cfg: dict):
    """Google Sheets 직원DB 자동 생성. spreadsheet_id 없으면 신규 생성."""
    sys.path.insert(0, str(Path.home() / '.claude/lib'))
    try:
        from google_auth import get_credentials
        from googleapiclient.discovery import build
    except ImportError:
        print("\n  ※ Google 라이브러리가 없어요.")
        print("    pip install google-api-python-client google-auth google-auth-oauthlib")
        print("    설치 후 다시 시도하거나, 직접 시트를 만들고 ID만 입력하세요.")
        return

    print("\n  Google 계정 인증 중... (브라우저가 열립니다)")
    creds = get_credentials([
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
    ])
    sheets = build('sheets', 'v4', credentials=creds)

    spreadsheet_id = cfg['google_workspace'].get('spreadsheet_id', '')

    if not spreadsheet_id:
        print("  새 Google Sheets 만드는 중...")
        body = {'properties': {'title': f"{cfg['company']['name']} 급여 관리"}}
        result = sheets.spreadsheets().create(body=body).execute()
        spreadsheet_id = result['spreadsheetId']
        print(f"  생성됨: {result['spreadsheetUrl']}")
        cfg['google_workspace']['spreadsheet_id'] = spreadsheet_id
        write_config(cfg)

    sheet_name = cfg['google_workspace']['sheets']['employees']
    meta = sheets.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    existing = [s['properties']['title'] for s in meta.get('sheets', [])]

    if sheet_name not in existing:
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]},
        ).execute()
        print(f"  시트 추가: {sheet_name}")

    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption='RAW',
        body={'values': [EMPLOYEE_DB_HEADERS]},
    ).execute()
    print(f"  헤더 입력 완료")
    print(f"  → 이제 시트를 열어서 직원 정보를 채우세요:")
    print(f"     https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")


def show_current():
    if not COMPANY_PATH.exists():
        print("\n  company.yaml 이 없어요. 먼저 setup.py 를 실행하세요.\n")
        return
    print()
    print("=" * 60)
    print(f"  현재 설정: {COMPANY_PATH}")
    print("=" * 60)
    with open(COMPANY_PATH, encoding='utf-8') as f:
        print(f.read())


def main():
    parser = argparse.ArgumentParser(description='Payroll 셋업 (초보자용)')
    parser.add_argument('--create-sheet', action='store_true',
                        help='회사 정보 입력 + Google Sheets 직원DB 자동 생성')
    parser.add_argument('--show', action='store_true', help='현재 설정 확인')
    args = parser.parse_args()

    if args.show:
        show_current()
        return

    cfg = build_config()
    write_config(cfg)

    if args.create_sheet:
        create_employee_sheet(cfg)
    else:
        print("\n  ※ Google Sheets 직원DB는 아직 안 만들어졌어요.")
        print("     다음 명령으로 자동 생성하실 수 있어요:")
        print("       python3 .claude/skills/payroll/scripts/setup.py --create-sheet")
        print("     (또는 직접 만드시고 setup.py 다시 실행해서 URL만 입력)")

    print()
    print("=" * 60)
    print("  셋업 완료 — 이제 매월 급여 처리를 시작할 수 있어요")
    print("=" * 60)
    print()
    print("  다음 단계:")
    print("    1) Google Sheets 직원DB에 직원 정보 입력")
    print("    2) 매월 28일~말일 사이에 Claude에게 이렇게 말하기:")
    print('         "이번 달 급여 처리하자"')
    print()
    print("  설정 변경이 필요하면:")
    print("    - 다시 셋업: python3 setup.py")
    print("    - 직접 수정: config/company.yaml 파일 열어서 편집")
    print()


if __name__ == '__main__':
    main()
