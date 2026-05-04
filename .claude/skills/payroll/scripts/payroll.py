#!/usr/bin/env python3
"""
급여 계산 스크립트 (한국 노동법/세무 기준)
4대보험료 및 소득세 계산, Google Sheets 급여대장 생성

회사 정보는 config/company.yaml에서 로드 (없으면 setup.py 안내).

Usage:
    python3 payroll.py generate 2026-01            # 급여대장 생성 (전 매장)
    python3 payroll.py generate 2026-01 본점        # 특정 매장만
    python3 payroll.py employees                    # 직원 목록 조회
    python3 payroll.py calculate 3000000           # 단순 계산 테스트
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import yaml

# 공유 인증 모듈
sys.path.insert(0, str(Path.home() / '.claude/lib'))
sys.path.insert(0, str(Path(__file__).parent))
from google_auth import get_credentials
from googleapiclient.discovery import build
from config_loader import load_config as _load_config

TAX_TABLE_PATH = Path(__file__).parent.parent / 'config' / 'income_tax_table.json'


def load_tax_table() -> List[Dict]:
    """간이세액표 로드"""
    if not TAX_TABLE_PATH.exists():
        return []
    with open(TAX_TABLE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_config() -> Dict:
    """설정 파일 로드 (company.yaml + rates-kr-2026.yaml 통합)"""
    return _load_config()


def get_sheets_service():
    """Google Sheets API 서비스"""
    creds = get_credentials()
    if not creds:
        print("Error: 인증 실패. 실행: python3 ~/.claude/lib/google_auth.py --auth")
        sys.exit(1)
    return build('sheets', 'v4', credentials=creds)


class PayrollCalculator:
    """급여 및 4대보험료/소득세 계산기"""

    def __init__(self, config: Dict):
        self.config = config
        self.insurance = config['insurance']
        self.tax = config['income_tax']
        self.exemption = config['tax_exemption']
        self.tax_table = load_tax_table()

    def calculate_national_pension(self, base_salary: int) -> int:
        """국민연금 계산 (근로자 부담분)"""
        np = self.insurance['national_pension']

        # 상/하한 적용
        taxable = max(np['floor'], min(base_salary, np['ceiling']))

        # 원단위 절사
        return int(taxable * np['employee_rate'] / 10) * 10

    def calculate_health_insurance(self, base_salary: int) -> tuple:
        """건강보험 + 장기요양보험 계산"""
        hi = self.insurance['health_insurance']
        ltc = self.insurance['long_term_care']

        # 건강보험료 (원단위 절사)
        health = int(base_salary * hi['employee_rate'] / 10) * 10

        # 장기요양보험료 (건강보험의 일정 비율, 원단위 절사)
        care = int(health * ltc['rate'] / 10) * 10

        return health, care

    def calculate_employment_insurance(self, base_salary: int) -> int:
        """고용보험 계산 (근로자 부담분)"""
        ei = self.insurance['employment_insurance']
        return int(base_salary * ei['employee_rate'] / 10) * 10

    def calculate_income_tax(self, taxable_income: int, dependents: int = 1) -> int:
        """소득세 계산 (국세청 간이세액표 기반)"""
        # 간이세액표 룩업
        if self.tax_table:
            dep_key = str(min(dependents, 11))  # 최대 11명까지

            for entry in self.tax_table:
                if entry['min'] <= taxable_income < entry['max']:
                    tax = entry['tax'].get(dep_key, 0)
                    return tax

            # 테이블 범위 초과 시 (500만원 이상)
            if taxable_income >= 5000000 and self.tax_table:
                last_entry = self.tax_table[-1]
                base_tax = last_entry['tax'].get(dep_key, 0)
                # 초과분에 대해 약 15% 추가 적용 (간략화)
                excess = taxable_income - last_entry['max']
                additional = int(excess * 0.15 / 10) * 10
                return base_tax + additional

            # 테이블 범위 미만 (100만원 미만) - 비과세
            if taxable_income < 1000000:
                return 0

        # 테이블 없으면 기존 방식 (fallback)
        brackets = self.tax['brackets']
        tax = 0
        for bracket in brackets:
            if taxable_income <= bracket['ceiling']:
                tax = int(taxable_income * bracket['rate'])
                break
        else:
            tax = int(taxable_income * brackets[-1]['rate'])

        deduction = (dependents - 1) * 12500 if dependents > 1 else 0
        return max(0, int((tax - deduction) / 10) * 10)

    def calculate_local_tax(self, income_tax: int) -> int:
        """지방소득세 계산 (소득세의 10%)"""
        return int(income_tax * self.tax['local_tax_rate'] / 10) * 10

    def calculate_all(self, base_salary: int, meal_allowance: int = 200000,
                      overtime: int = 0, dependents: int = 1) -> Dict:
        """전체 급여 계산"""

        # 지급 항목
        gross_pay = base_salary + meal_allowance + overtime

        # 4대보험 (기본급 + 추가수당 기준, 식대는 비과세)
        insurance_base = base_salary + overtime

        national_pension = self.calculate_national_pension(insurance_base)
        health, care = self.calculate_health_insurance(insurance_base)
        employment = self.calculate_employment_insurance(insurance_base)

        # 소득세 (비과세 식대 제외)
        taxable = gross_pay - min(meal_allowance, self.exemption['meal_allowance'])
        income_tax = self.calculate_income_tax(taxable, dependents)
        local_tax = self.calculate_local_tax(income_tax)

        # 총 공제
        total_deduction = (national_pension + health + care +
                          employment + income_tax + local_tax)

        # 실지급액
        net_pay = gross_pay - total_deduction

        return {
            'base_salary': base_salary,
            'meal_allowance': meal_allowance,
            'overtime': overtime,
            'gross_pay': gross_pay,
            'national_pension': national_pension,
            'health_insurance': health,
            'long_term_care': care,
            'employment_insurance': employment,
            'income_tax': income_tax,
            'local_tax': local_tax,
            'total_deduction': total_deduction,
            'net_pay': net_pay
        }


class PayrollManager:
    """급여대장 관리"""

    def __init__(self):
        self.config = load_config()
        self.calculator = PayrollCalculator(self.config)
        self.service = get_sheets_service()
        self.spreadsheet_id = self.config['google_sheets'].get('spreadsheet_id', '')

        if not self.spreadsheet_id:
            print("Warning: spreadsheet_id가 설정되지 않았습니다.")
            print("config/company.yaml의 google_workspace.spreadsheet_id를 채워주세요.")

    def get_employees(self, branch: Optional[str] = None) -> List[Dict]:
        """직원 목록 조회"""
        if not self.spreadsheet_id:
            return []

        sheet_name = self.config['google_sheets']['sheets']['employees']

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_name
        ).execute()

        values = result.get('values', [])
        if len(values) < 2:
            return []

        # 헤더와 데이터 분리
        headers = values[0]
        employees = []

        for row in values[1:]:
            emp = dict(zip(headers, row + [''] * (len(headers) - len(row))))

            # 퇴사일이 없는 재직자만
            if emp.get('퇴사일', ''):
                continue

            # 매장 필터
            if branch and emp.get('매장', '') != branch:
                continue

            employees.append(emp)

        return employees

    def generate_payroll(self, year_month: str, branch: Optional[str] = None) -> Dict:
        """월별 급여대장 생성"""
        employees = self.get_employees(branch)

        if not employees:
            return {'error': '직원 데이터가 없습니다.', 'employees': []}

        results = []
        total_gross = 0
        total_deduction = 0
        total_net = 0

        for emp in employees:
            try:
                base_salary = int(emp.get('기본급', 0) or 0)
                meal = int(emp.get('식대', 200000) or 200000)
                overtime = int(emp.get('추가수당', 0) or 0)
                dependents = int(emp.get('부양가족수', 1) or 1)
            except ValueError:
                continue

            if base_salary == 0:
                continue

            calc = self.calculator.calculate_all(base_salary, meal, overtime, dependents)

            result = {
                '이름': emp.get('이름', ''),
                '매장': emp.get('매장', ''),
                **calc
            }
            results.append(result)

            total_gross += calc['gross_pay']
            total_deduction += calc['total_deduction']
            total_net += calc['net_pay']

        return {
            'year_month': year_month,
            'branch': branch or '전체',
            'employee_count': len(results),
            'total_gross': total_gross,
            'total_deduction': total_deduction,
            'total_net': total_net,
            'employees': results
        }

    def save_to_sheet(self, year_month: str, payroll_data: Dict, by_branch: bool = False) -> bool:
        """급여대장을 Google Sheets에 저장

        Args:
            year_month: 대상 월 (YYYY-MM)
            payroll_data: 급여 데이터
            by_branch: True면 매장별 시트 분리, False면 단일 시트
        """
        if not self.spreadsheet_id:
            print("Error: spreadsheet_id가 설정되지 않았습니다.")
            return False

        # 헤더
        headers = ['이름', '매장', '기본급', '식대', '추가수당', '지급총액',
                   '국민연금', '건강보험', '장기요양', '고용보험',
                   '소득세', '지방소득세', '공제총액', '실지급액']

        try:
            # 시트 목록 조회
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]

            if by_branch:
                # 매장별 시트 분리
                branches = {}
                for emp in payroll_data['employees']:
                    branch = emp['매장']
                    if branch not in branches:
                        branches[branch] = []
                    branches[branch].append(emp)

                for branch, employees in branches.items():
                    sheet_name = f"{year_month}_{branch}"
                    self._save_branch_sheet(sheet_name, headers, employees, existing_sheets)
                    print(f"  저장: {sheet_name} ({len(employees)}명)")

                # 전체 합계 시트도 생성
                sheet_name = f"{year_month}_전체"
                self._save_branch_sheet(sheet_name, headers, payroll_data['employees'], existing_sheets)
                print(f"  저장: {sheet_name} (전체 {len(payroll_data['employees'])}명)")

            else:
                # 단일 시트 (기존 방식)
                sheet_name = f"{year_month}_급여대장"
                self._save_branch_sheet(sheet_name, headers, payroll_data['employees'], existing_sheets)

            return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    def _save_branch_sheet(self, sheet_name: str, headers: List[str],
                           employees: List[Dict], existing_sheets: List[str]) -> None:
        """개별 시트에 데이터 저장"""
        # 데이터 행
        rows = [headers]
        for emp in employees:
            rows.append([
                emp['이름'],
                emp['매장'],
                emp['base_salary'],
                emp['meal_allowance'],
                emp['overtime'],
                emp['gross_pay'],
                emp['national_pension'],
                emp['health_insurance'],
                emp['long_term_care'],
                emp['employment_insurance'],
                emp['income_tax'],
                emp['local_tax'],
                emp['total_deduction'],
                emp['net_pay']
            ])

        # 합계 행
        rows.append([
            '합계', '',
            sum(e['base_salary'] for e in employees),
            sum(e['meal_allowance'] for e in employees),
            sum(e['overtime'] for e in employees),
            sum(e['gross_pay'] for e in employees),
            sum(e['national_pension'] for e in employees),
            sum(e['health_insurance'] for e in employees),
            sum(e['long_term_care'] for e in employees),
            sum(e['employment_insurance'] for e in employees),
            sum(e['income_tax'] for e in employees),
            sum(e['local_tax'] for e in employees),
            sum(e['total_deduction'] for e in employees),
            sum(e['net_pay'] for e in employees)
        ])

        # 시트가 없으면 생성
        if sheet_name not in existing_sheets:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    'requests': [{
                        'addSheet': {
                            'properties': {'title': sheet_name}
                        }
                    }]
                }
            ).execute()
            existing_sheets.append(sheet_name)

        # 데이터 쓰기
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption='USER_ENTERED',
            body={'values': rows}
        ).execute()


def cmd_generate(args):
    """급여대장 생성"""
    manager = PayrollManager()

    print(f"\n=== {args.year_month} 급여대장 생성 ===\n")

    payroll = manager.generate_payroll(args.year_month, args.branch)

    if 'error' in payroll:
        print(f"Error: {payroll['error']}")
        return

    # 결과 출력
    print(f"대상: {payroll['branch']}")
    print(f"직원 수: {payroll['employee_count']}명")
    print(f"지급총액: {payroll['total_gross']:,}원")
    print(f"공제총액: {payroll['total_deduction']:,}원")
    print(f"실지급액: {payroll['total_net']:,}원")

    print("\n--- 직원별 내역 ---")
    for emp in payroll['employees']:
        print(f"\n{emp['이름']} ({emp['매장']})")
        print(f"  기본급: {emp['base_salary']:,} + 식대: {emp['meal_allowance']:,}")
        print(f"  지급총액: {emp['gross_pay']:,} - 공제: {emp['total_deduction']:,}")
        print(f"  실지급액: {emp['net_pay']:,}")

    # Google Sheets 저장
    if args.save:
        print("\n--- Google Sheets 저장 ---")
        if manager.save_to_sheet(args.year_month, payroll, by_branch=args.by_branch):
            if args.by_branch:
                print(f"저장 완료: {args.year_month}_[매장별] + {args.year_month}_전체")
            else:
                print(f"저장 완료: {args.year_month}_급여대장")
        else:
            print("저장 실패")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(payroll, indent=2, ensure_ascii=False))


def cmd_employees(args):
    """직원 목록 조회"""
    manager = PayrollManager()
    employees = manager.get_employees(args.branch)

    if not employees:
        print("직원 데이터가 없습니다.")
        return

    print(f"\n=== 직원 목록 ({len(employees)}명) ===\n")

    for emp in employees:
        print(f"{emp.get('이름', 'N/A')} | {emp.get('매장', 'N/A')} | "
              f"{emp.get('직급', 'N/A')} | 기본급: {emp.get('기본급', 'N/A')}")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(employees, indent=2, ensure_ascii=False))


def cmd_calculate(args):
    """단순 계산 테스트"""
    config = load_config()
    calc = PayrollCalculator(config)

    result = calc.calculate_all(
        base_salary=args.salary,
        meal_allowance=args.meal,
        overtime=args.overtime,
        dependents=args.dependents
    )

    print(f"\n=== 급여 계산 결과 ===\n")
    print(f"기본급: {result['base_salary']:,}원")
    print(f"식대: {result['meal_allowance']:,}원")
    print(f"추가수당: {result['overtime']:,}원")
    print(f"지급총액: {result['gross_pay']:,}원")
    print()
    print(f"국민연금: {result['national_pension']:,}원")
    print(f"건강보험: {result['health_insurance']:,}원")
    print(f"장기요양: {result['long_term_care']:,}원")
    print(f"고용보험: {result['employment_insurance']:,}원")
    print(f"소득세: {result['income_tax']:,}원")
    print(f"지방소득세: {result['local_tax']:,}원")
    print(f"공제총액: {result['total_deduction']:,}원")
    print()
    print(f"실지급액: {result['net_pay']:,}원")

    if args.json:
        print("\n--- JSON ---")
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='IMI 급여 관리')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # generate
    gen_parser = subparsers.add_parser('generate', help='급여대장 생성')
    gen_parser.add_argument('year_month', help='대상 월 (YYYY-MM)')
    gen_parser.add_argument('branch', nargs='?', help='매장명 (생략시 전체)')
    gen_parser.add_argument('--save', action='store_true', help='Google Sheets 저장')
    gen_parser.add_argument('--by-branch', action='store_true', help='매장별 시트 분리')
    gen_parser.add_argument('--json', action='store_true', help='JSON 출력')

    # employees
    emp_parser = subparsers.add_parser('employees', help='직원 목록')
    emp_parser.add_argument('--branch', help='매장 필터')
    emp_parser.add_argument('--json', action='store_true', help='JSON 출력')

    # calculate
    calc_parser = subparsers.add_parser('calculate', help='급여 계산 테스트')
    calc_parser.add_argument('salary', type=int, help='기본급')
    calc_parser.add_argument('--meal', type=int, default=200000, help='식대')
    calc_parser.add_argument('--overtime', type=int, default=0, help='추가수당')
    calc_parser.add_argument('--dependents', type=int, default=1, help='부양가족수')
    calc_parser.add_argument('--json', action='store_true', help='JSON 출력')

    args = parser.parse_args()

    if args.command == 'generate':
        cmd_generate(args)
    elif args.command == 'employees':
        cmd_employees(args)
    elif args.command == 'calculate':
        cmd_calculate(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
