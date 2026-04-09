"""
BPT 신선대감만터미널 AX 데모용 더미 데이터 생성
random.seed(42) - 재현 가능
UTF-8 BOM 없음
"""

import csv
import random
from datetime import date, time, timedelta, datetime

random.seed(42)

BASE_DIR = "/home/rhim/claude-projects/do-better-workspace/50-resources/sample-data/bpt"


# ─────────────────────────────────────────────────
# CSV 1: bpt_vessel_operations_2603.csv (~200행)
# ─────────────────────────────────────────────────

def gen_vessel_operations():
    rows = []

    shipping_lines = [
        ("HMM", 0.35),
        ("MSC", 0.12),
        ("Evergreen", 0.10),
        ("ONE", 0.10),
        ("MSK", 0.08),
        ("CMA CGM", 0.08),
        ("Yang Ming", 0.06),
        ("ZIM", 0.04),
        ("PIL", 0.03),
        ("Wan Hai", 0.02),
        ("SM Line", 0.02),
    ]

    vessel_pool = {
        "HMM": ["HMM Algeciras", "HMM Rotterdam", "HMM Gdansk", "HMM Copenhagen", "HMM Oslo", "HMM Stockholm"],
        "MSC": ["MSC Oscar", "MSC Gulsun", "MSC Isabella", "MSC Eloane", "MSC Mia"],
        "Evergreen": ["Ever Ace", "Ever Alot", "Ever Art", "Ever Atop", "Ever Atop"],
        "ONE": ["ONE Apus", "ONE Stork", "ONE Hawk", "ONE Crane", "ONE Falcon"],
        "MSK": ["Maersk Essen", "Maersk Elba", "Maersk Emden", "Maersk Enfield"],
        "CMA CGM": ["CMA CGM Jacques Saade", "CMA CGM Antoine de Saint Exupery", "CMA CGM Palais Royal"],
        "Yang Ming": ["Yang Ming Witness", "Yang Ming Warrant", "Yang Ming Wellness"],
        "ZIM": ["ZIM Samson", "ZIM Shenzhen", "ZIM São Paulo"],
        "PIL": ["PIL Halong Bay", "PIL Mekong River"],
        "Wan Hai": ["Wan Hai 505", "Wan Hai 508"],
        "SM Line": ["SM Busan", "SM Seoul"],
    }

    # 터미널/선석 배분: 신선대 70%, 감만 30%
    terminal_data = {
        "신선대": ["S1", "S2", "S3", "S4", "S5"],
        "감만": ["G1", "G2", "G3"],
    }

    delay_reasons = ["기상악화", "장비고장", "하역사 교대", "선사 지연", "세관 검사"]

    start_date = date(2026, 3, 1)
    end_date = date(2026, 3, 31)
    total_days = (end_date - start_date).days + 1

    # 선사별 누적 콜 수 배분 (~200행 목표)
    total_calls = 202
    line_names = [sl[0] for sl in shipping_lines]
    line_weights = [sl[1] for sl in shipping_lines]
    assigned_lines = random.choices(line_names, weights=line_weights, k=total_calls)

    call_counter = 1
    for i, line in enumerate(assigned_lines):
        call_id = f"VC-2603-{call_counter:03d}"
        call_counter += 1

        vessel = random.choice(vessel_pool[line])

        # 터미널
        terminal = random.choices(["신선대", "감만"], weights=[0.70, 0.30])[0]
        berth_no = random.choice(terminal_data[terminal])

        # 날짜
        arr_day = start_date + timedelta(days=random.randint(0, total_days - 1))
        arr_time = f"{random.randint(0, 23):02d}:{random.choice(['00','15','30','45'])}"

        # 항박 시간: 12~96시간
        stay_hours = random.randint(12, 96)
        dep_dt = datetime.combine(arr_day, datetime.strptime(arr_time, "%H:%M").time()) + timedelta(hours=stay_hours)
        dep_day = dep_dt.date()
        dep_time = dep_dt.strftime("%H:%M")

        # 크레인 수
        cranes = random.randint(2, 5)

        # 3월 중순 기상악화 집중: 3/12~3/19
        is_weather_period = date(2026, 3, 12) <= arr_day <= date(2026, 3, 19)

        # delay
        if is_weather_period and random.random() < 0.55:
            delay_hours = round(random.uniform(2.0, 6.0), 1)
            delay_reason = "기상악화"
        elif random.random() < 0.3:
            delay_hours = round(random.uniform(0.5, 4.0), 1)
            delay_reason = random.choice(delay_reasons[1:])  # 기상악화 제외
        else:
            delay_hours = 0.0
            delay_reason = "없음"

        # GMPH 25~35, gross_hours 역산
        gmph = random.uniform(25, 35)
        total_moves = random.randint(500, 4000)
        gross_hours = round(total_moves / (gmph * cranes), 1)
        net_hours = round(gross_hours - delay_hours, 1)

        # TEU 배분
        # load + discharge ≈ total_moves (오차 ±5%)
        load_ratio = random.uniform(0.35, 0.65)
        load_teu = int(total_moves * load_ratio)
        discharge_teu = total_moves - load_teu

        # 환적: 전체의 ~50%
        ts_teu = int(total_moves * random.uniform(0.40, 0.60))

        # 냉동: 5~8%
        reefer_count = int(total_moves * random.uniform(0.05, 0.08))

        # 위험물: 8~12%
        dg_count = int(total_moves * random.uniform(0.08, 0.12))

        # LOA: 200~400m
        vessel_loa = random.randint(200, 400)

        # 마지막 5건 진행중
        status = "진행중" if call_counter > total_calls - 3 else "완료"

        rows.append({
            "vessel_call_id": call_id,
            "vessel_name": vessel,
            "shipping_line": line,
            "terminal": terminal,
            "berth_no": berth_no,
            "arrival_date": arr_day.isoformat(),
            "arrival_time": arr_time,
            "departure_date": dep_day.isoformat(),
            "departure_time": dep_time,
            "sts_cranes_assigned": cranes,
            "total_moves": total_moves,
            "gross_hours": gross_hours,
            "net_hours": max(net_hours, 0.1),
            "delay_hours": delay_hours,
            "delay_reason": delay_reason,
            "load_teu": load_teu,
            "discharge_teu": discharge_teu,
            "ts_teu": ts_teu,
            "reefer_count": reefer_count,
            "dg_count": dg_count,
            "vessel_loa": vessel_loa,
            "status": status,
        })

    path = f"{BASE_DIR}/bpt_vessel_operations_2603.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"생성 완료: {path} ({len(rows)}행)")


# ─────────────────────────────────────────────────
# CSV 2: bpt_equipment_master.csv (~45행)
# ─────────────────────────────────────────────────

def gen_equipment_master():
    rows = []

    equip_configs = [
        # (prefix, count, type, terminal, manufacturers)
        ("STS", 8, "STS Crane", None, ["ZPMC", "Liebherr"]),
        ("ARMGC", 20, "ARMGC", None, ["ZPMC", "Konecranes"]),
        ("YT", 12, "Yard Tractor", None, ["Kalmar", "Konecranes"]),
        ("RS", 5, "Reach Stacker", None, ["Kalmar", "Liebherr"]),
    ]

    # STS: 신선대 5 / 감만 3
    sts_terminals = ["신선대"] * 5 + ["감만"] * 3
    # ARMGC: 신선대 13 / 감만 7
    armgc_terminals = ["신선대"] * 13 + ["감만"] * 7
    # YT: 신선대 8 / 감만 4
    yt_terminals = ["신선대"] * 8 + ["감만"] * 4
    # RS: 신선대 3 / 감만 2
    rs_terminals = ["신선대"] * 3 + ["감만"] * 2

    terminal_map = {
        "STS": sts_terminals,
        "ARMGC": armgc_terminals,
        "YT": yt_terminals,
        "RS": rs_terminals,
    }

    today = date(2026, 4, 9)

    for prefix, count, etype, _, manufacturers in equip_configs:
        terminals = terminal_map[prefix]
        for i in range(count):
            equip_id = f"{prefix}-{i+1:02d}"
            terminal = terminals[i]
            manufacturer = random.choice(manufacturers)

            # 설치연도: 2005~2024
            year_installed = random.randint(2005, 2024)
            age = 2026 - year_installed

            # 노후도 반영
            mtbf = max(150, int(600 - age * 15) + random.randint(-30, 30))
            mttr = min(15, int(2 + age * 0.4) + random.randint(-1, 2))

            if etype == "STS Crane":
                monthly_ops = random.randint(350, 600)
                monthly_moves = random.randint(4000, 9000)
            elif etype == "ARMGC":
                monthly_ops = random.randint(300, 550)
                monthly_moves = random.randint(3000, 7000)
            elif etype == "Yard Tractor":
                monthly_ops = random.randint(200, 450)
                monthly_moves = random.randint(2000, 5000)
            else:  # Reach Stacker
                monthly_ops = random.randint(150, 300)
                monthly_moves = random.randint(800, 2000)

            # 정비 상태: 80% 정상
            r = random.random()
            if r < 0.80:
                maint_status = "정상"
            elif r < 0.90:
                maint_status = "점검예정"
            else:
                maint_status = "수리중"

            # 최근 PM: 30~120일 전
            last_pm_days_ago = random.randint(30, 120)
            last_pm_date = (today - timedelta(days=last_pm_days_ago)).isoformat()

            # 다음 PM: 30~90일 후
            next_pm_days = random.randint(15, 90)
            next_pm_date = (today + timedelta(days=next_pm_days)).isoformat()

            rows.append({
                "equipment_id": equip_id,
                "equipment_type": etype,
                "terminal": terminal,
                "manufacturer": manufacturer,
                "year_installed": year_installed,
                "monthly_operating_hours": monthly_ops,
                "monthly_moves": monthly_moves,
                "mtbf_hours": mtbf,
                "mttr_hours": mttr,
                "maintenance_status": maint_status,
                "last_pm_date": last_pm_date,
                "next_pm_date": next_pm_date,
            })

    path = f"{BASE_DIR}/bpt_equipment_master.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"생성 완료: {path} ({len(rows)}행)")


# ─────────────────────────────────────────────────
# CSV 3: bpt_yard_daily_2603.csv (~930행)
# 31일 x 30블록
# ─────────────────────────────────────────────────

def gen_yard_daily():
    rows = []

    start_date = date(2026, 3, 1)

    # 블록 정의
    blocks = []
    # A01~A15: 신선대 일반/냉동/위험물
    for i in range(1, 16):
        label = f"A{i:02d}"
        if i in [13, 14, 15]:
            btype = "위험물"
        elif i in [11, 12]:
            btype = "빈컨테이너"
        else:
            btype = "일반"
        blocks.append((label, "신선대", btype, random.randint(380, 500)))

    # B01~B10: 감만 일반/빈컨테이너
    for i in range(1, 11):
        label = f"B{i:02d}"
        if i in [9, 10]:
            btype = "빈컨테이너"
        else:
            btype = "일반"
        blocks.append((label, "감만", btype, random.randint(300, 420)))

    # R01~R05: 냉동전용 (신선대)
    for i in range(1, 6):
        label = f"R{i:02d}"
        blocks.append((label, "신선대", "냉동", random.randint(200, 320)))

    for day_offset in range(31):
        current_date = start_date + timedelta(days=day_offset)
        # 3월 중순 기상악화: 야드 점유율 약간 상승
        is_weather = date(2026, 3, 12) <= current_date <= date(2026, 3, 19)

        for (blk_name, terminal, btype, capacity) in blocks:
            # 점유율
            if btype == "냉동":
                occ_ratio = random.uniform(0.80, 0.94) if is_weather else random.uniform(0.75, 0.92)
            elif btype == "위험물":
                occ_ratio = random.uniform(0.55, 0.75)
            elif btype == "빈컨테이너":
                occ_ratio = random.uniform(0.40, 0.65)
            else:
                occ_ratio = random.uniform(0.65, 0.85) if is_weather else random.uniform(0.60, 0.78)

            current_teu = int(capacity * occ_ratio)

            # 일일 반입/반출
            gate_in = random.randint(20, 80)
            gate_out = random.randint(15, 75)

            # 평균 체류일
            if btype == "냉동":
                avg_dwell = round(random.uniform(2.0, 4.0), 1)
            elif btype == "빈컨테이너":
                avg_dwell = round(random.uniform(3.0, 6.0), 1)
            else:
                avg_dwell = round(random.uniform(3.5, 7.0), 1)

            # 장치료 초과
            containers_over_freetime = int(current_teu * random.uniform(0.03, 0.10))

            # 냉동 블록 전용
            if btype == "냉동":
                reefer_capacity_val = capacity
                reefer_plugged = current_teu
                temp_alarm_count = random.randint(0, 3) if random.random() < 0.25 else 0
            else:
                reefer_capacity_val = ""
                reefer_plugged = ""
                temp_alarm_count = ""

            rows.append({
                "date": current_date.isoformat(),
                "yard_block": blk_name,
                "terminal": terminal,
                "block_type": btype,
                "capacity_teu": capacity,
                "current_teu": current_teu,
                "gate_in": gate_in,
                "gate_out": gate_out,
                "avg_dwell_days": avg_dwell,
                "containers_over_freetime": containers_over_freetime,
                "reefer_plugged": reefer_plugged,
                "reefer_capacity": reefer_capacity_val,
                "temp_alarm_count": temp_alarm_count,
            })

    path = f"{BASE_DIR}/bpt_yard_daily_2603.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"생성 완료: {path} ({len(rows)}행)")


# ─────────────────────────────────────────────────
# CSV 4: bpt_billing_summary_2603.csv (~22행)
# ─────────────────────────────────────────────────

def gen_billing_summary():
    # 선사별 기준 물동량 (TEU)
    teu_base = {
        "HMM": 28000,
        "MSC": 9500,
        "Evergreen": 8000,
        "ONE": 7800,
        "MSK": 6500,
        "CMA CGM": 6200,
        "Yang Ming": 4800,
        "ZIM": 3200,
        "PIL": 2400,
        "Wan Hai": 1600,
        "SM Line": 1600,
    }

    # 할인율 정의
    discount_rate = {
        "HMM": 0.08,
        "MSK": 0.10,
        "MSC": 0.10,
        "Evergreen": 0.12,
        "ONE": 0.12,
        "CMA CGM": 0.12,
        "Yang Ming": 0.13,
        "ZIM": 0.14,
        "PIL": 0.15,
        "Wan Hai": 0.15,
        "SM Line": 0.15,
    }

    # dispute 설정
    dispute_cases = {
        ("MSK", "하반기"): ("Y", "물량 불일치"),
        ("Evergreen", "상반기"): ("Y", "장치료 기간 이의"),
        ("Yang Ming", "하반기"): ("Y", "물량 불일치"),
        ("Wan Hai", "하반기"): ("Y", "냉동료 산정 이의"),
    }

    # 미입금/부분입금
    unpaid_cases = {
        ("MSK", "상반기"), ("MSK", "하반기"),
        ("ONE", "상반기"),
        ("Yang Ming", "하반기"),
        ("SM Line", "하반기"),
    }
    partial_cases = {
        ("Evergreen", "상반기"),
        ("Wan Hai", "하반기"),
    }

    rows = []
    inv_counter = 1

    billing_date = date(2026, 3, 31)
    due_date_base = date(2026, 4, 15)

    for line in teu_base:
        base_teu = teu_base[line]
        disc = discount_rate[line]

        for period in ["상반기", "하반기"]:
            inv_id = f"INV-2603-{inv_counter:03d}"
            inv_counter += 1

            # 상반기/하반기 물동량 분배 (±10% 변동)
            half_ratio = random.uniform(0.45, 0.55)
            if period == "상반기":
                teu_vol = int(base_teu * half_ratio)
            else:
                teu_vol = int(base_teu * (1 - half_ratio))

            # 하역료: TEU * 13만원 * (1-할인율)
            stev_fee = int(teu_vol * 13 * (1 - disc))

            # 장치료: 15% 초과분 * 3~5일 * 0.8~1.2만원
            over_teu = int(teu_vol * 0.15)
            storage_fee = int(over_teu * random.randint(3, 5) * random.uniform(0.8, 1.2))

            # 냉동료: 6% * 4~6일 * 3~4만원
            reefer_teu = int(teu_vol * 0.06)
            reefer_fee = int(reefer_teu * random.randint(4, 6) * random.uniform(3, 4))

            # 위험물 처리료: 10% * 1.5~2.5만원
            dg_teu = int(teu_vol * 0.10)
            dg_fee = int(dg_teu * random.uniform(1.5, 2.5))

            # 재취급료: 3% * 0.5~1만원
            rehandling_teu = int(teu_vol * 0.03)
            rehandling_fee = int(rehandling_teu * random.uniform(0.5, 1.0))

            total_amount = stev_fee + storage_fee + reefer_fee + dg_fee + rehandling_fee

            # 결제 상태
            key = (line, period)
            if key in unpaid_cases:
                payment_status = "미입금"
            elif key in partial_cases:
                payment_status = "부분입금"
            else:
                payment_status = "입금완료"

            # due date: 상반기 4/10, 하반기 4/25
            if period == "상반기":
                due_dt = date(2026, 4, 10).isoformat()
            else:
                due_dt = date(2026, 4, 25).isoformat()

            # dispute
            if key in dispute_cases:
                d_flag, d_reason = dispute_cases[key]
            else:
                d_flag = "N"
                d_reason = "없음"

            rows.append({
                "billing_id": inv_id,
                "shipping_line": line,
                "billing_period": f"2026-03 {period}",
                "stevedoring_fee": stev_fee,
                "storage_fee": storage_fee,
                "reefer_fee": reefer_fee,
                "dg_handling_fee": dg_fee,
                "rehandling_fee": rehandling_fee,
                "total_amount": total_amount,
                "payment_status": payment_status,
                "payment_due_date": due_dt,
                "dispute_flag": d_flag,
                "dispute_reason": d_reason,
                "teu_volume": teu_vol,
            })

    path = f"{BASE_DIR}/bpt_billing_summary_2603.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"생성 완료: {path} ({len(rows)}행)")


if __name__ == "__main__":
    gen_vessel_operations()
    gen_equipment_master()
    gen_yard_daily()
    gen_billing_summary()
    print("\n전체 생성 완료.")
