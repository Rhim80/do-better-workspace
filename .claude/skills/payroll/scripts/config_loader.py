"""
Payroll config loader

회사별 정보(company.yaml) + 한국 표준 요율(rates-kr-2026.yaml) + 간이세액표를
하나로 로드하여 기존 스크립트가 기대하는 형태로 반환.

- company.yaml: 회사명/매장/세무사/Google Sheets ID 등 (.gitignore)
- rates-kr-2026.yaml: 4대보험 요율, 가산수당, 두루누리 등 (공개)
- income_tax_table.json: 간이세액표 334구간 (공개)
"""

from pathlib import Path
import sys
import yaml

CONFIG_DIR = Path(__file__).parent.parent / 'config'

COMPANY_PATH = CONFIG_DIR / 'company.yaml'
COMPANY_EXAMPLE_PATH = CONFIG_DIR / 'company.yaml.example'
RATES_PATH = CONFIG_DIR / 'rates-kr-2026.yaml'
INCOME_TAX_PATH = CONFIG_DIR / 'income_tax_table.json'


def load_config() -> dict:
    """모든 config을 통합 로드.

    반환 구조 (기존 스크립트 호환):
      {
        'company': {...},                  # company.yaml
        'accountant': {...},               # company.yaml
        'sender': {...},                   # company.yaml
        'paths': {...},                    # company.yaml
        'salary_structure': {...},         # rates
        'allowances': {...},               # rates
        'insurance': {...},                # rates
        'durumuri': {...},                 # rates
        'tax_exemption': {...},            # rates
        'income_tax': {...},               # rates
        'retirement': {...},               # rates
        # 호환성 키 (기존 코드가 참조)
        'google_sheets': {                 # company.google_workspace의 alias
          'spreadsheet_id': '...',
          'sheets': {...},
        },
        'output': {                        # company.paths의 alias
          'pkm_base': '',
          'excel_folder': '...',
          'payroll_record': '...',
        },
        'business': {                      # company의 alias
          'name': '...',
          'branches': [...],
          ...
        },
      }
    """
    if not COMPANY_PATH.exists():
        print(
            f"\n[setup 필요] company.yaml이 없습니다.\n"
            f"  1) cp {COMPANY_EXAMPLE_PATH.name} {COMPANY_PATH.name}\n"
            f"  2) {COMPANY_PATH} 의 placeholder를 채워주세요.\n"
            f"  또는 대화형 셋업: python3 {Path(__file__).parent / 'setup.py'}\n",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(COMPANY_PATH, encoding='utf-8') as f:
        company_cfg = yaml.safe_load(f) or {}

    if not RATES_PATH.exists():
        print(f"Error: {RATES_PATH} 가 없습니다.", file=sys.stderr)
        sys.exit(1)

    with open(RATES_PATH, encoding='utf-8') as f:
        rates_cfg = yaml.safe_load(f) or {}

    cfg: dict = {}
    cfg.update(rates_cfg)
    cfg.update(company_cfg)

    gw = company_cfg.get('google_workspace', {})
    cfg['google_sheets'] = {
        'spreadsheet_id': gw.get('spreadsheet_id', ''),
        'sheets': gw.get('sheets', {}),
    }

    paths = company_cfg.get('paths', {})
    cfg['output'] = {
        'pkm_base': paths.get('output_base', ''),
        'excel_folder': paths.get('excel_folder', '{year}/세무사자료'),
        'payroll_record': paths.get('payroll_record', '{year}/급여변동'),
    }

    return cfg


def get_branches(cfg: dict) -> list:
    """매장 목록 반환. 단일 사업장이면 빈 배열."""
    return cfg.get('company', {}).get('branches', []) or []


def get_branch_prefix(cfg: dict) -> dict:
    """매장명 → 시트명 약어 매핑. 매핑 없으면 매장명 그대로."""
    mapping = cfg.get('company', {}).get('branch_prefix', {}) or {}
    branches = get_branches(cfg)
    return {b: mapping.get(b, b) for b in branches}


def is_single_site(cfg: dict) -> bool:
    """단일 사업장 모드 여부 (매장 분리 없이 한 시트로 처리)."""
    return len(get_branches(cfg)) == 0


def get_company_short(cfg: dict) -> str:
    """회사 약칭 (퇴직금 파일명·양식용). 없으면 정식명."""
    company = cfg.get('company', {})
    return company.get('short_name') or company.get('name', '회사')


def get_business_owner(cfg: dict) -> str:
    """사업주명 (퇴직금산정내역서 양식용)."""
    return cfg.get('company', {}).get('business_owner', '')


def resolve_path(cfg: dict, key: str, year: str | int) -> Path:
    """paths config의 템플릿 경로를 절대 경로로 해석.

    key: 'excel_folder' | 'payroll_record' | 'resignation_folder' 등
    {year} placeholder 자동 치환.
    """
    base_str = cfg.get('paths', {}).get('output_base', '') \
               or cfg.get('output', {}).get('pkm_base', '')
    base = Path(base_str).expanduser() if base_str else Path.cwd()
    if not base.is_absolute():
        base = Path.cwd() / base

    template = cfg.get('paths', {}).get(key) \
               or cfg.get('output', {}).get(key, '')
    if not template:
        return base

    sub = str(template).format(year=year)
    return base / sub
