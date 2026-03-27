#!/usr/bin/env python3
"""CSV data quality cleaner for Claude Code.

Usage:
  python csv-clean.py <csv_file> [options]

Options:
  --info                  Data quality analysis only (no changes)
  --remove-subtotals      Remove subtotal/total rows
  --clean-numbers         Clean number formatting (commas, currency, percent)
  --clean-numbers-cols C  Clean numbers in specific columns only (comma-separated)
  --normalize-dates       Normalize date formats (default: YYYY-MM-DD)
  --date-format FMT       Target date format (default: %Y-%m-%d)
  --date-cols COLS        Date normalization target columns (comma-separated)
  --unpivot ID1,ID2       Keep ID columns, unpivot the rest
  --value-name NAME       Value column name for unpivot (default: value)
  --variable-name NAME    Variable column name for unpivot (default: variable)
  --normalize-text COL=MAPFILE  Normalize text using mapping file
  --output PATH           Output file path
  --inplace               Overwrite original file
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas not installed. Run: pip install pandas>=2.0.0", file=sys.stderr)
    sys.exit(1)


def _is_string_dtype(series):
    """Check if a pandas Series has string/object dtype (compatible with pandas 2.x and 3.x)."""
    return pd.api.types.is_string_dtype(series) or series.dtype == object


# --- Subtotal Detection & Removal ---

SUBTOTAL_KEYWORDS_EXACT = ["계", "sum"]  # exact match only (avoid "회계", "설계", "계약")
SUBTOTAL_KEYWORDS_PARTIAL = [
    "소계", "합계", "총계", "총합",
    "subtotal", "total", "grand total",
]


def detect_subtotal_rows(df):
    """Detect rows containing subtotal/total keywords in the first text column."""
    results = []
    # Find the first column that contains string data
    check_cols = []
    for col in df.columns:
        if _is_string_dtype(df[col]):
            check_cols.append(col)
        if len(check_cols) >= 3:
            break

    if not check_cols:
        return results

    for idx, row in df.iterrows():
        for col in check_cols:
            val = str(row[col]).strip().lower() if pd.notna(row[col]) else ""
            if not val:
                continue
            matched_kw = None
            # Partial match keywords (safe - "소계" won't appear in normal words)
            for kw in SUBTOTAL_KEYWORDS_PARTIAL:
                if kw in val:
                    matched_kw = kw
                    break
            # Exact match keywords (e.g., "계" must be the entire cell value)
            if not matched_kw:
                for kw in SUBTOTAL_KEYWORDS_EXACT:
                    if val == kw:
                        matched_kw = kw
                        break
            if matched_kw:
                results.append({"row": idx, "keyword": matched_kw, "value": str(row[col]).strip()})
                break

    return results


def remove_subtotal_rows(df):
    """Remove rows containing subtotal/total keywords. Returns (cleaned_df, removed_count)."""
    detected = detect_subtotal_rows(df)
    if not detected:
        return df, 0

    rows_to_remove = [d["row"] for d in detected]
    cleaned = df.drop(index=rows_to_remove).reset_index(drop=True)
    return cleaned, len(rows_to_remove)


# --- Number Cleaning ---

NUMBER_PATTERNS = re.compile(r'^[\s]*[$\u20a9\u00a5\u20ac\u00a3]?[\s]*[\d,]+\.?\d*[\s]*%?[\s]*$')
CURRENCY_SYMBOLS = re.compile(r'[$\u20a9\u00a5\u20ac\u00a3]')


def detect_text_numbers(df):
    """Detect columns with formatted numbers (commas, currency symbols, percent)."""
    results = {}
    for col in df.columns:
        if not _is_string_dtype(df[col]):
            continue
        samples = []
        for val in df[col].dropna().head(100):
            s = str(val).strip()
            if not s:
                continue
            # Check for comma-separated numbers, currency symbols, or percent
            has_comma = "," in s and any(c.isdigit() for c in s)
            has_currency = bool(CURRENCY_SYMBOLS.search(s))
            has_percent = s.endswith("%") and any(c.isdigit() for c in s)
            if has_comma or has_currency or has_percent:
                samples.append(s)
        if samples:
            results[col] = samples[:5]
    return results


def clean_numbers(df, columns=None):
    """Clean number formatting in specified or auto-detected columns."""
    if columns is None:
        detected = detect_text_numbers(df)
        columns = list(detected.keys())

    if not columns:
        return df, 0

    cleaned_count = 0
    for col in columns:
        if col not in df.columns:
            print(f"  Warning: column '{col}' not found, skipping", file=sys.stderr)
            continue

        def clean_val(val):
            if pd.isna(val):
                return val
            s = str(val).strip()
            if not s:
                return val
            # Remove currency symbols
            s = CURRENCY_SYMBOLS.sub("", s)
            # Remove percent sign (keep number)
            s = s.rstrip("%").strip()
            # Remove commas
            s = s.replace(",", "")
            s = s.strip()
            # Try converting to number
            try:
                return pd.to_numeric(s)
            except (ValueError, TypeError):
                return val

        original = df[col].copy()
        df[col] = df[col].apply(clean_val)
        changed = (original != df[col]).sum()
        cleaned_count += changed

    return df, cleaned_count


# --- Date Normalization ---

DATE_PATTERNS = [
    (re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$'), "%Y-%m-%d"),
    (re.compile(r'^\d{4}\.\d{1,2}\.\d{1,2}\.?$'), "%Y.%m.%d"),
    (re.compile(r'^\d{4}/\d{1,2}/\d{1,2}$'), "%Y/%m/%d"),
    (re.compile(r'^\d{4}\ub144\s*\d{1,2}\uc6d4\s*\d{1,2}\uc77c$'), None),  # YYYY년 M월 D일
    (re.compile(r'^\d{2}\.\d{1,2}\.\d{1,2}$'), "%y.%m.%d"),
    (re.compile(r'^\d{8}$'), "%Y%m%d"),
]


def parse_date_value(val):
    """Try to parse a date value. Returns datetime or None."""
    from datetime import datetime

    s = str(val).strip().rstrip(".")
    if not s:
        return None

    for pattern, fmt in DATE_PATTERNS:
        if pattern.match(s):
            if fmt is None:
                # Korean format: YYYY년 M월 D일
                m = re.match(r'(\d{4})\ub144\s*(\d{1,2})\uc6d4\s*(\d{1,2})\uc77c', s)
                if m:
                    try:
                        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                    except ValueError:
                        return None
            else:
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    continue
    return None


def detect_date_columns(df):
    """Detect columns with date-like values and their format distribution."""
    results = {}
    for col in df.columns:
        if not _is_string_dtype(df[col]):
            continue
        format_counts = {}
        total_checked = 0
        for val in df[col].dropna().head(100):
            s = str(val).strip()
            if not s:
                continue
            total_checked += 1
            for pattern, fmt in DATE_PATTERNS:
                if pattern.match(s.rstrip(".")):
                    label = fmt if fmt else "YYYY년M월D일"
                    format_counts[label] = format_counts.get(label, 0) + 1
                    break

        if format_counts and sum(format_counts.values()) >= total_checked * 0.3:
            results[col] = {
                "formats": format_counts,
                "total": total_checked,
            }
    return results


def normalize_dates(df, columns=None, target_format="%Y-%m-%d"):
    """Normalize date formats in specified or auto-detected columns."""
    if columns is None:
        detected = detect_date_columns(df)
        columns = list(detected.keys())

    if not columns:
        return df, 0

    normalized_count = 0
    warnings = []
    for col in columns:
        if col not in df.columns:
            print(f"  Warning: column '{col}' not found, skipping", file=sys.stderr)
            continue

        def normalize_val(val):
            nonlocal normalized_count, warnings
            if pd.isna(val):
                return val
            parsed = parse_date_value(val)
            if parsed:
                normalized_count += 1
                return parsed.strftime(target_format)
            return val

        df[col] = df[col].apply(normalize_val)

    return df, normalized_count


# --- Crosstab / Unpivot ---

MONTH_PATTERNS = [
    re.compile(r'^\d{1,2}\uc6d4$'),     # 1월, 12월
    re.compile(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', re.I),
    re.compile(r'^\d{4}[-/.]\d{1,2}$'),  # 2024-01, 2024.01
    re.compile(r'^[qQ][1-4]$'),           # Q1-Q4
    re.compile(r'^\d{1,2}\ubd84\uae30$'), # 1분기
]


def detect_crosstab(df):
    """Detect if headers suggest a pivot/crosstab structure."""
    cols = [str(c) for c in df.columns]
    matched = []
    for c in cols:
        for p in MONTH_PATTERNS:
            if p.match(c.strip()):
                matched.append(c)
                break

    if len(matched) >= 3:
        return {"pattern_cols": matched, "description": "month/quarter pattern"}
    return None


def unpivot_data(df, id_columns, variable_name="variable", value_name="value"):
    """Unpivot (melt) a crosstab DataFrame."""
    missing = [c for c in id_columns if c not in df.columns]
    if missing:
        print(f"ERROR: ID columns not found: {', '.join(missing)}", file=sys.stderr)
        print(f"Available columns: {', '.join(df.columns)}", file=sys.stderr)
        sys.exit(1)

    value_cols = [c for c in df.columns if c not in id_columns]
    melted = pd.melt(df, id_vars=id_columns, value_vars=value_cols,
                     var_name=variable_name, value_name=value_name)
    return melted


# --- Text Normalization ---

def normalize_text(df, column, mapping):
    """Normalize text values using a mapping dictionary."""
    if column not in df.columns:
        print(f"  Warning: column '{column}' not found, skipping", file=sys.stderr)
        return df, 0

    count = 0

    def apply_mapping(val):
        nonlocal count
        if pd.isna(val):
            return val
        s = str(val).strip()
        # Exact match first
        if s in mapping:
            count += 1
            return mapping[s]
        # Case-insensitive match
        s_lower = s.lower()
        for k, v in mapping.items():
            if k.lower() == s_lower:
                count += 1
                return v
        return val

    df[column] = df[column].apply(apply_mapping)
    return df, count


def load_mapping_file(filepath):
    """Load a mapping file (CSV or JSON)."""
    ext = Path(filepath).suffix.lower()
    if ext == ".json":
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    elif ext == ".csv":
        mapping = {}
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    mapping[row[0].strip()] = row[1].strip()
        return mapping
    else:
        print(f"ERROR: Unsupported mapping file format: {ext}", file=sys.stderr)
        sys.exit(1)


# --- Data Quality Analysis ---

def analyze_data_quality(df):
    """Analyze CSV data quality and print suggestions."""
    print("--- Data Quality Analysis ---")
    found_issues = False

    # 1. Subtotal rows
    subtotals = detect_subtotal_rows(df)
    if subtotals:
        found_issues = True
        kw_counts = {}
        for s in subtotals:
            kw_counts[s["keyword"]] = kw_counts.get(s["keyword"], 0) + 1
        kw_str = ", ".join(f"{k}({v})" for k, v in kw_counts.items())
        row_nums = ", ".join(str(s["row"] + 2) for s in subtotals[:10])  # +2 for header + 0-index
        print(f"[SUBTOTAL_ROWS] {len(subtotals)} rows contain keywords: {kw_str}. Rows: {row_nums}")
        print(f"  -> Suggested: --remove-subtotals")
        print()

    # 2. Text numbers
    text_nums = detect_text_numbers(df)
    if text_nums:
        found_issues = True
        col_names = ", ".join(f"'{c}'" for c in text_nums.keys())
        samples = []
        for col, vals in list(text_nums.items())[:3]:
            samples.extend(vals[:2])
        sample_str = ", ".join(f'"{s}"' for s in samples[:4])
        print(f"[TEXT_NUMBERS] Columns {col_names} contain formatted numbers (e.g., {sample_str})")
        cols_arg = ",".join(text_nums.keys())
        print(f"  -> Suggested: --clean-numbers or --clean-numbers-cols {cols_arg}")
        print()

    # 3. Date formats
    dates = detect_date_columns(df)
    if dates:
        found_issues = True
        for col, info in dates.items():
            fmt_parts = []
            for fmt, cnt in info["formats"].items():
                pct = int(cnt / info["total"] * 100)
                fmt_parts.append(f"{fmt}({pct}%)")
            print(f"[DATE_FORMATS] Column '{col}' has mixed formats: {', '.join(fmt_parts)}")
        date_cols = ",".join(dates.keys())
        print(f"  -> Suggested: --normalize-dates --date-cols {date_cols}")
        print()

    # 4. Crosstab
    crosstab = detect_crosstab(df)
    if crosstab:
        found_issues = True
        cols_str = ", ".join(crosstab["pattern_cols"][:6])
        if len(crosstab["pattern_cols"]) > 6:
            cols_str += "..."
        # Suggest ID columns (non-pattern columns)
        pattern_set = set(crosstab["pattern_cols"])
        id_cols = [c for c in df.columns if c not in pattern_set]
        id_str = ",".join(id_cols[:3])
        print(f"[CROSSTAB] Headers suggest pivot structure: {cols_str}")
        print(f"  -> Suggested: --unpivot {id_str}")
        print()

    if not found_issues:
        print("No data quality issues detected.")
        print()

    # Summary stats
    print(f"--- Summary ---")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"Headers: {', '.join(str(c) for c in df.columns[:10])}", end="")
    if len(df.columns) > 10:
        print(f" ... and {len(df.columns) - 10} more")
    else:
        print()


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="CSV data quality cleaner")
    parser.add_argument("csv_file", help="CSV file path")
    parser.add_argument("--info", action="store_true", help="Data quality analysis only")
    parser.add_argument("--remove-subtotals", action="store_true", help="Remove subtotal/total rows")
    parser.add_argument("--clean-numbers", action="store_true", help="Clean number formatting")
    parser.add_argument("--clean-numbers-cols", help="Specific columns for number cleaning (comma-separated)")
    parser.add_argument("--normalize-dates", action="store_true", help="Normalize date formats")
    parser.add_argument("--date-format", default="%Y-%m-%d", help="Target date format")
    parser.add_argument("--date-cols", help="Date columns (comma-separated)")
    parser.add_argument("--unpivot", help="ID columns to keep (comma-separated), unpivot the rest")
    parser.add_argument("--value-name", default="value", help="Value column name for unpivot")
    parser.add_argument("--variable-name", default="variable", help="Variable column name for unpivot")
    parser.add_argument("--normalize-text", action="append",
                        help="COL=MAPFILE format for text normalization")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--inplace", action="store_true", help="Overwrite original file")

    args = parser.parse_args()
    csv_path = os.path.abspath(args.csv_file)

    if not os.path.exists(csv_path):
        print(f"ERROR: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    # Read CSV
    try:
        df = pd.read_csv(csv_path, dtype=str)
    except Exception as e:
        print(f"ERROR: Failed to read CSV: {e}", file=sys.stderr)
        sys.exit(1)

    original_rows = len(df)
    print(f"File: {csv_path}")
    print(f"Loaded: {original_rows} rows x {len(df.columns)} columns")
    print()

    # Info mode
    if args.info:
        analyze_data_quality(df)
        return

    # Check if any operation requested
    has_operation = any([
        args.remove_subtotals,
        args.clean_numbers,
        args.clean_numbers_cols,
        args.normalize_dates,
        args.unpivot,
        args.normalize_text,
    ])

    if not has_operation:
        print("No operations specified. Use --info to analyze, or specify operations.")
        print("Available: --remove-subtotals, --clean-numbers, --normalize-dates, --unpivot")
        return

    changes = []

    # 1. Remove subtotals
    if args.remove_subtotals:
        df, removed = remove_subtotal_rows(df)
        changes.append(f"Removed {removed} subtotal rows")

    # 2. Clean numbers
    num_cols = None
    if args.clean_numbers_cols:
        num_cols = [c.strip() for c in args.clean_numbers_cols.split(",")]
        df, cleaned = clean_numbers(df, num_cols)
        changes.append(f"Cleaned {cleaned} number values in columns: {', '.join(num_cols)}")
    elif args.clean_numbers:
        df, cleaned = clean_numbers(df)
        changes.append(f"Cleaned {cleaned} number values (auto-detected columns)")

    # 3. Normalize dates
    date_cols = None
    if args.date_cols:
        date_cols = [c.strip() for c in args.date_cols.split(",")]
    if args.normalize_dates:
        df, normalized = normalize_dates(df, date_cols, args.date_format)
        changes.append(f"Normalized {normalized} date values -> {args.date_format}")

    # 4. Text normalization
    if args.normalize_text:
        for spec in args.normalize_text:
            if "=" not in spec:
                print(f"ERROR: --normalize-text format: COL=MAPFILE, got: {spec}", file=sys.stderr)
                sys.exit(1)
            col, mapfile = spec.split("=", 1)
            mapping = load_mapping_file(mapfile)
            df, count = normalize_text(df, col, mapping)
            changes.append(f"Normalized {count} text values in column '{col}'")

    # 5. Unpivot (should be last as it changes structure)
    if args.unpivot:
        id_columns = [c.strip() for c in args.unpivot.split(",")]
        df = unpivot_data(df, id_columns, args.variable_name, args.value_name)
        changes.append(f"Unpivoted: ID columns [{', '.join(id_columns)}] -> {len(df)} rows")

    # Determine output path
    if args.inplace:
        out_path = csv_path
    elif args.output:
        out_path = os.path.abspath(args.output)
    else:
        stem = Path(csv_path).stem
        ext = Path(csv_path).suffix
        out_path = os.path.join(os.path.dirname(csv_path), f"{stem}_cleaned{ext}")

    # Write output
    df.to_csv(out_path, index=False, encoding="utf-8")

    # Report
    print("--- Changes Applied ---")
    for c in changes:
        print(f"  {c}")
    print()
    print(f"Result: {len(df)} rows x {len(df.columns)} columns")
    print(f"Output: {out_path}")

    # Preview
    print()
    print("Preview (first 5 rows):")
    preview = df.head(5).to_string(index=False, max_colwidth=30)
    for line in preview.split("\n"):
        print(f"  {line}")


if __name__ == "__main__":
    main()
