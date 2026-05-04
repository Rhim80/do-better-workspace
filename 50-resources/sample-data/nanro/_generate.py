"""
난로회 부트캠프 시나리오용 더미데이터 생성기.

가상의 한식당 "청기와옥" (청담동 본점, 한정식 + 주류) 2026-03 ~ 2026-04 (2개월) 데이터.

산출 파일:
1. menu_master.csv          — 메뉴 마스터 (38개 SKU, 원가/판매가/배달앱가)
2. pos_sales_2603.csv       — 3월 홀(POS) 매출 (~2,400건)
3. pos_sales_2604.csv       — 4월 홀(POS) 매출 (~2,500건)
4. delivery_sales_2603.csv  — 3월 배달앱 매출 (~900건, 배민/쿠팡이츠)
5. delivery_sales_2604.csv  — 4월 배달앱 매출 (~1,050건)
6. daily_summary.csv        — 일자별 마감 요약 (61일, 보고서 시나리오용)

Mission 1 = menu_master + pos + delivery 교차 (채널·메뉴별 수익성)
Mission 2 = daily_summary + 어제 데이터 → 모닝 브리프
"""

from __future__ import annotations

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(__file__).parent
random.seed(20260504)

# ---------------------------------------------------------------------------
# 1. 메뉴 마스터
# ---------------------------------------------------------------------------
# 카테고리: 식사(한정식/단품), 사이드, 주류, 음료, 디저트
# 가격구조: 정가(매장가) > 배민가(같거나 +500~1,000원) > 쿠팡이츠가(같거나 +500~1,000원)
# 수수료: 배민 6.8% + 결제2.7% + 광고 5% / 쿠팡이츠 9.8% + 결제2.7%
# 배달비: 사장 3,500 + 손님 3,000 (둘 다 별도 정산)

MENU = [
    # SKU, 카테고리, 메뉴명, 원가, 매장가, 배민가, 쿠팡이츠가, 메인주력
    # === 식사 (한정식 코스) ===
    ("M001", "코스", "청기와 한정식 (1인)",        16500, 39000, 39000, 39000, True),
    ("M002", "코스", "청기와 프리미엄 한정식 (1인)", 24000, 59000, None,  None,  True),
    ("M003", "코스", "런치 한상 (1인, 평일점심)",   9800,  19000, 19000, 19000, True),
    # === 식사 (단품) ===
    ("S001", "식사", "갈비탕",                     7800,  19000, 20000, 20000, True),
    ("S002", "식사", "한우육개장",                 8200,  21000, 22000, 22000, True),
    ("S003", "식사", "묵은지등갈비찜 (소)",        12500, 38000, 39000, 39000, True),
    ("S004", "식사", "묵은지등갈비찜 (대)",        21000, 58000, 59000, 59000, False),
    ("S005", "식사", "간장게장 정식",              14000, 32000, 33000, 33000, True),
    ("S006", "식사", "양념게장 정식",              13500, 31000, 32000, 32000, False),
    ("S007", "식사", "보쌈 (소)",                  11000, 32000, 33000, 33000, True),
    ("S008", "식사", "보쌈 (대)",                  19500, 52000, 53000, 53000, False),
    ("S009", "식사", "한우 육회비빔밥",            10500, 22000, 23000, 23000, True),
    ("S010", "식사", "들기름 막국수",              4200,  13000, 13500, 13500, True),
    ("S011", "식사", "메밀전병",                   3800,  14000, 14500, 14500, False),
    ("S012", "식사", "전복죽",                     6800,  18000, 18500, 18500, False),
    # === 사이드 ===
    ("D001", "사이드", "한치회무침",                7800,  22000, 22500, 22500, False),
    ("D002", "사이드", "수육 (소)",                 8500,  26000, 26500, 26500, False),
    ("D003", "사이드", "감자전",                    3200,  14000, 14500, 14500, True),
    ("D004", "사이드", "해물파전",                  4500,  17000, 17500, 17500, True),
    ("D005", "사이드", "한우 떡갈비 (2장)",         9800,  24000, 24500, 24500, False),
    ("D006", "사이드", "계란말이",                  2400,  9000,  9500,  9500,  False),
    ("D007", "사이드", "도토리묵",                  2800,  11000, 11500, 11500, False),
    # === 주류 (배달 X) ===
    ("A001", "주류", "참이슬 후레쉬",               1200,  5000,  None,  None,  True),
    ("A002", "주류", "처음처럼",                    1200,  5000,  None,  None,  False),
    ("A003", "주류", "테라",                        1500,  6000,  None,  None,  True),
    ("A004", "주류", "카스",                        1500,  6000,  None,  None,  False),
    ("A005", "주류", "한라산",                      4500,  14000, None,  None,  False),
    ("A006", "주류", "복분자주 (병)",               6800,  22000, None,  None,  False),
    ("A007", "주류", "막걸리 (병)",                 1800,  8000,  8500,  8500,  False),
    ("A008", "주류", "전통주 페어링 코스",          18000, 49000, None,  None,  False),
    # === 음료 ===
    ("B001", "음료", "사이다",                      900,   4000,  4500,  4500,  False),
    ("B002", "음료", "콜라",                        900,   4000,  4500,  4500,  False),
    ("B003", "음료", "수정과",                      1200,  5000,  5500,  5500,  False),
    ("B004", "음료", "식혜",                        1200,  5000,  5500,  5500,  False),
    ("B005", "음료", "오미자차",                    1500,  6000,  6500,  6500,  False),
    # === 디저트 ===
    ("E001", "디저트", "흑임자 아이스크림",         1800,  7000,  7500,  7500,  False),
    ("E002", "디저트", "약과 3종",                  1500,  6000,  6500,  6500,  False),
    ("E003", "디저트", "쌍화차",                    1800,  7000,  7500,  7500,  False),
    ("E004", "디저트", "수제 한과 모듬",            2400,  9000,  9500,  9500,  False),
]

# 배달앱 수수료 (실제 업계 평균치)
COMMISSION = {
    "매장": {"app": 0.0,  "pg": 0.0},
    "배민": {"app": 0.068, "pg": 0.027, "ad": 0.05},   # 오픈리스트형 가정
    "쿠팡이츠": {"app": 0.098, "pg": 0.027, "ad": 0.0}, # 스마트요금제 가정 (광고 X)
}
# 배달비 (사장 부담만 기록)
DELIVERY_OWNER_FEE = {"배민": 3500, "쿠팡이츠": 3500}


def write_menu_master():
    path = OUT / "menu_master.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "SKU", "카테고리", "메뉴명", "원가",
            "매장가", "배민가", "쿠팡이츠가",
            "배달가능", "주력메뉴",
            "배민_앱수수료율", "배민_PG수수료율", "배민_광고수수료율", "배민_사장배달비",
            "쿠팡이츠_앱수수료율", "쿠팡이츠_PG수수료율", "쿠팡이츠_사장배달비",
        ])
        for sku, cat, name, cost, store, baemin, coupang, hero in MENU:
            deliverable = "Y" if baemin is not None else "N"
            w.writerow([
                sku, cat, name, cost,
                store,
                baemin if baemin is not None else "",
                coupang if coupang is not None else "",
                deliverable,
                "Y" if hero else "N",
                COMMISSION["배민"]["app"], COMMISSION["배민"]["pg"], COMMISSION["배민"].get("ad", 0), DELIVERY_OWNER_FEE["배민"],
                COMMISSION["쿠팡이츠"]["app"], COMMISSION["쿠팡이츠"]["pg"], DELIVERY_OWNER_FEE["쿠팡이츠"],
            ])
    print(f"[OK] {path.name}: {len(MENU)} rows")


# ---------------------------------------------------------------------------
# 2. 매출 데이터 헬퍼
# ---------------------------------------------------------------------------

WEEKDAY_LABEL = ["월", "화", "수", "목", "금", "토", "일"]
HOLIDAY_2603 = {date(2026, 3, 1), date(2026, 3, 2)}  # 삼일절 + 대체
HOLIDAY_2604 = {date(2026, 4, 30)}                   # 부처님오신날 가정
# 매장 정기휴무: 일요일은 영업, 매월 첫째·셋째 월요일 휴무
def is_closed(d: date) -> bool:
    if d.weekday() == 0 and d.day <= 21:  # 첫째·셋째 월요일 (대략)
        # 첫째 월요일
        if d.day <= 7:
            return True
        # 셋째 월요일
        if 15 <= d.day <= 21:
            return True
    return False


def weekday_weight(d: date) -> float:
    """요일 가중치. 금/토 강세, 일/화 약."""
    return [0.9, 0.85, 0.95, 1.05, 1.45, 1.50, 1.05][d.weekday()]


def daily_orders_target(d: date, channel: str, month: int) -> int:
    """일자/채널별 평균 주문 수 목표."""
    if is_closed(d):
        return 0
    base_pos = 95 if month == 3 else 102      # 4월 +7% 트래픽 (봄 회복)
    base_del = 32 if month == 3 else 38       # 4월 +18% 배달 성장 (광고 시작)
    base = base_pos if channel == "POS" else base_del
    target = base * weekday_weight(d)
    if d in HOLIDAY_2603 or d in HOLIDAY_2604:
        target *= 0.55  # 공휴일 청담 점심 급감
    # 4/12 일요일 카니발(가정) 등 특이일
    if d == date(2026, 4, 12):
        target *= 1.35  # 인스타 바이럴
    if d == date(2026, 4, 25):
        target *= 0.5   # 폭우
    return max(1, int(round(target * random.uniform(0.85, 1.15))))


# ---------------------------------------------------------------------------
# 3. POS 매출 (홀)
# ---------------------------------------------------------------------------
HALL_HOUR_WEIGHT = [
    # 0~11
    0,0,0,0,0,0,0,0,0,0,0,3,
    # 12~23
    14,18,8,3,2,3,12,18,16,10,6,3,
]
DINE_PARTY_DIST = [(2, 0.35), (3, 0.18), (4, 0.22), (5, 0.10), (6, 0.08), (8, 0.05), (10, 0.02)]


def pick_hall_hour():
    return random.choices(range(24), weights=HALL_HOUR_WEIGHT, k=1)[0]


def pick_party():
    n = [p for p, _ in DINE_PARTY_DIST]
    w = [w for _, w in DINE_PARTY_DIST]
    return random.choices(n, weights=w, k=1)[0]


def hall_basket(hour: int, party: int) -> list[tuple[str, int]]:
    """
    한 테이블 주문. 점심·저녁 다른 메뉴 패턴.
    return: [(SKU, qty), ...]
    """
    basket: dict[str, int] = {}

    if 11 <= hour <= 14:  # 점심
        # 메인 (인당 1)
        for _ in range(party):
            sku = random.choices(
                ["M003", "S001", "S002", "S009", "S010", "S005", "M001"],
                weights=[28, 18, 12, 14, 10, 8, 10], k=1
            )[0]
            basket[sku] = basket.get(sku, 0) + 1
        # 사이드 살짝
        if party >= 3 and random.random() < 0.45:
            side = random.choice(["D003", "D004", "D006", "D007"])
            basket[side] = basket.get(side, 0) + 1
        # 음료 점심엔 30%만
        if random.random() < 0.30:
            drink = random.choice(["B001", "B002", "B003", "B004", "B005"])
            basket[drink] = basket.get(drink, 0) + min(party, 2)

    else:  # 저녁
        # 코스 vs 단품 분기
        if party <= 3 and random.random() < 0.18:
            # 코스
            sku = random.choices(["M001", "M002"], weights=[70, 30], k=1)[0]
            basket[sku] = party
            # 주류
            if random.random() < 0.7:
                a = random.choices(["A001", "A003", "A005", "A006", "A008"], weights=[30, 25, 12, 18, 15], k=1)[0]
                basket[a] = basket.get(a, 0) + random.randint(1, 2)
        else:
            # 단품 코스 (메인 1~2 + 사이드 + 주류)
            mains = random.sample(["S003", "S005", "S007", "S009", "S002", "S001"], k=random.randint(1, 2))
            for m in mains:
                # 등갈비찜·보쌈은 사이즈 분기
                if m == "S003" and party >= 4:
                    m = "S004"
                if m == "S007" and party >= 4:
                    m = "S008"
                basket[m] = basket.get(m, 0) + 1
            sides = random.sample(["D001", "D002", "D003", "D004", "D005", "D006", "D007"], k=random.randint(1, 3))
            for s in sides:
                basket[s] = basket.get(s, 0) + 1
            # 주류
            n_drink = max(1, party // 2)
            for _ in range(n_drink):
                a = random.choices(
                    ["A001", "A002", "A003", "A004", "A005", "A006", "A007"],
                    weights=[28, 12, 25, 12, 8, 8, 7], k=1)[0]
                basket[a] = basket.get(a, 0) + random.randint(1, 2)
            # 음료
            if random.random() < 0.4:
                drink = random.choice(["B001", "B002", "B003", "B004"])
                basket[drink] = basket.get(drink, 0) + random.randint(1, 2)
        # 디저트 (저녁만, 25%)
        if random.random() < 0.25:
            dessert = random.choice(["E001", "E002", "E003", "E004"])
            basket[dessert] = basket.get(dessert, 0) + 1

    return list(basket.items())


PAYMENT_METHODS = [
    ("카드", 0.78),
    ("간편결제", 0.16),  # 카카오페이/네이버페이/제로페이
    ("현금", 0.04),
    ("계좌이체", 0.02),
]


def write_pos_sales(month: int):
    fname = f"pos_sales_26{month:02d}.csv"
    path = OUT / fname
    menu_lookup = {sku: (cat, name, cost, store) for sku, cat, name, cost, store, *_ in MENU}

    rows: list[list] = []
    last_day = (date(2026, month + 1, 1) - timedelta(days=1)).day if month != 12 else 31

    seq = 0
    for d in (date(2026, month, day) for day in range(1, last_day + 1)):
        n = daily_orders_target(d, "POS", month)
        for _ in range(n):
            seq += 1
            hour = pick_hall_hour()
            minute = random.randint(0, 59)
            party = pick_party()
            order_no = f"P-{d:%y%m%d}-{seq:04d}"
            payment = random.choices([p for p, _ in PAYMENT_METHODS], weights=[w for _, w in PAYMENT_METHODS], k=1)[0]

            for sku, qty in hall_basket(hour, party):
                cat, name, cost, store_price = menu_lookup[sku]
                rows.append([
                    order_no,
                    d.isoformat(),
                    f"{hour:02d}:{minute:02d}",
                    WEEKDAY_LABEL[d.weekday()],
                    party,
                    sku, cat, name, qty,
                    store_price, store_price * qty,
                    cost * qty,
                    payment,
                ])

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "주문번호", "주문일", "주문시간", "요일", "인원수",
            "SKU", "카테고리", "메뉴명", "수량",
            "단가", "합계", "원가합계", "결제수단",
        ])
        w.writerows(rows)
    n_orders = len({r[0] for r in rows})
    print(f"[OK] {fname}: {len(rows):,} lines / {n_orders:,} orders")


# ---------------------------------------------------------------------------
# 4. 배달 매출
# ---------------------------------------------------------------------------
DELIVERY_HOUR_WEIGHT = [
    0,0,0,0,0,0,0,0,0,0,0,8,
    16,12,5,2,2,4,12,18,14,5,2,0,
]
DELIVERY_PARTY = [(1, 0.35), (2, 0.40), (3, 0.15), (4, 0.10)]


def pick_delivery_hour():
    return random.choices(range(24), weights=DELIVERY_HOUR_WEIGHT, k=1)[0]


def pick_delivery_party():
    n = [p for p, _ in DELIVERY_PARTY]
    w = [w for _, w in DELIVERY_PARTY]
    return random.choices(n, weights=w, k=1)[0]


def delivery_basket(party: int, channel: str) -> list[tuple[str, int]]:
    """배달 주문 1건. 주류/코스 X."""
    deliverable = [sku for sku, *rest in MENU if (rest[3] if channel == "배민" else rest[4]) is not None and rest[1] != "코스" and rest[1] != "주류"]
    basket: dict[str, int] = {}

    # 메인 1~2개
    main_pool = ["S001", "S002", "S003", "S005", "S007", "S009", "S010", "S012"]
    if party >= 3:
        main_pool += ["S004", "S008"]
    n_main = 1 if party <= 2 else random.choice([1, 2])
    for _ in range(n_main):
        m = random.choice(main_pool)
        basket[m] = basket.get(m, 0) + 1
    # 사이드
    if random.random() < 0.55:
        side_pool = [s for s in ["D003", "D004", "D006", "D007"] if s in deliverable]
        if side_pool:
            s = random.choice(side_pool)
            basket[s] = basket.get(s, 0) + 1
    # 음료
    if random.random() < 0.32:
        d = random.choice(["B001", "B002", "B003", "B004"])
        basket[d] = basket.get(d, 0) + party
    # 막걸리 (배달 가능 주류)
    if random.random() < 0.18:
        basket["A007"] = basket.get("A007", 0) + 1
    return list(basket.items())


def write_delivery_sales(month: int):
    fname = f"delivery_sales_26{month:02d}.csv"
    path = OUT / fname
    menu_lookup = {sku: (cat, name, cost, store, baemin, coupang)
                   for sku, cat, name, cost, store, baemin, coupang, _ in MENU}

    rows: list[list] = []
    last_day = (date(2026, month + 1, 1) - timedelta(days=1)).day if month != 12 else 31

    seq_b, seq_c = 0, 0
    for d in (date(2026, month, day) for day in range(1, last_day + 1)):
        n = daily_orders_target(d, "DELIVERY", month)
        for _ in range(n):
            # 채널 분배 (4월에 쿠팡이츠 광고 시작 가정 → 4월 비중 35→48%)
            if month == 3:
                channel = random.choices(["배민", "쿠팡이츠"], weights=[65, 35], k=1)[0]
            else:
                channel = random.choices(["배민", "쿠팡이츠"], weights=[52, 48], k=1)[0]
            hour = pick_delivery_hour()
            minute = random.randint(0, 59)
            party = pick_delivery_party()

            if channel == "배민":
                seq_b += 1
                order_no = f"BM-{d:%y%m%d}-{seq_b:04d}"
            else:
                seq_c += 1
                order_no = f"CE-{d:%y%m%d}-{seq_c:04d}"

            order_total = 0
            order_cost = 0
            line_rows: list[list] = []
            for sku, qty in delivery_basket(party, channel):
                cat, name, cost, store_price, baemin_p, coupang_p = menu_lookup[sku]
                price = baemin_p if channel == "배민" else coupang_p
                if price is None:
                    price = store_price
                line_total = int(price) * qty
                order_total += line_total
                order_cost += cost * qty
                line_rows.append([
                    order_no,
                    d.isoformat(),
                    f"{hour:02d}:{minute:02d}",
                    WEEKDAY_LABEL[d.weekday()],
                    channel,
                    party,
                    sku, cat, name, qty,
                    int(price), line_total,
                    cost * qty,
                ])

            # 최소주문금액 적용 (12,000원)
            if order_total < 12000:
                # 다시 주력 단품 추가
                add_sku = random.choice(["S001", "S010"])
                cat, name, cost, store_price, baemin_p, coupang_p = menu_lookup[add_sku]
                price = baemin_p if channel == "배민" else coupang_p
                price = price or store_price
                line_rows.append([
                    order_no, d.isoformat(), f"{hour:02d}:{minute:02d}",
                    WEEKDAY_LABEL[d.weekday()], channel, party,
                    add_sku, cat, name, 1, int(price), int(price), cost,
                ])
                order_total += int(price)
                order_cost += cost

            # 수수료/배달비 계산
            comm = COMMISSION[channel]
            app_fee = round(order_total * comm["app"])
            pg_fee = round(order_total * comm["pg"])
            ad_fee = round(order_total * comm.get("ad", 0))
            owner_delivery = DELIVERY_OWNER_FEE[channel]
            net_revenue = order_total - app_fee - pg_fee - ad_fee - owner_delivery

            for r in line_rows:
                # 마지막 컬럼들에 주문 단위 정보 부가
                rows.append(r + [
                    order_total, order_cost,
                    app_fee, pg_fee, ad_fee, owner_delivery, net_revenue,
                ])

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "주문번호", "주문일", "주문시간", "요일", "채널", "인원수",
            "SKU", "카테고리", "메뉴명", "수량",
            "단가", "합계", "원가합계",
            "주문총액", "주문원가합계",
            "앱수수료", "PG수수료", "광고수수료", "사장배달비분담", "정산순매출",
        ])
        w.writerows(rows)

    n_orders = len({r[0] for r in rows})
    print(f"[OK] {fname}: {len(rows):,} lines / {n_orders:,} orders")


# ---------------------------------------------------------------------------
# 5. 일자별 마감 요약 (Mission 2 보고서용)
# ---------------------------------------------------------------------------

def build_daily_summary():
    """
    위에서 생성한 POS·DELIVERY CSV를 읽어 일자별 요약을 다시 만든다.
    Mission 2(모닝 브리프)는 이 한 파일만으로도 동작 가능하도록 설계.
    """
    summary: dict[date, dict] = {}

    for month in (3, 4):
        # POS 집계
        pos_path = OUT / f"pos_sales_26{month:02d}.csv"
        if pos_path.exists():
            with pos_path.open(encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    d = date.fromisoformat(r["주문일"])
                    rec = summary.setdefault(d, _new_daily(d))
                    rec["pos_orders"].add(r["주문번호"])
                    rec["pos_sales"] += int(r["합계"])
                    rec["pos_cost"] += int(r["원가합계"])
                    if r["카테고리"] == "주류":
                        rec["주류_매출"] += int(r["합계"])
                    elif r["카테고리"] == "코스":
                        rec["코스_매출"] += int(r["합계"])
        # DELIVERY 집계
        del_path = OUT / f"delivery_sales_26{month:02d}.csv"
        if del_path.exists():
            with del_path.open(encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    d = date.fromisoformat(r["주문일"])
                    rec = summary.setdefault(d, _new_daily(d))
                    if r["채널"] == "배민":
                        rec["bm_orders"].add(r["주문번호"])
                        rec["bm_sales"] += int(r["합계"])
                        rec["bm_app_fee"] += int(r["앱수수료"]) if r["주문번호"] not in rec["bm_seen"] else 0
                        rec["bm_pg_fee"] += int(r["PG수수료"]) if r["주문번호"] not in rec["bm_seen"] else 0
                        rec["bm_ad_fee"] += int(r["광고수수료"]) if r["주문번호"] not in rec["bm_seen"] else 0
                        rec["bm_owner_del"] += int(r["사장배달비분담"]) if r["주문번호"] not in rec["bm_seen"] else 0
                        rec["bm_seen"].add(r["주문번호"])
                    else:
                        rec["ce_orders"].add(r["주문번호"])
                        rec["ce_sales"] += int(r["합계"])
                        rec["ce_app_fee"] += int(r["앱수수료"]) if r["주문번호"] not in rec["ce_seen"] else 0
                        rec["ce_pg_fee"] += int(r["PG수수료"]) if r["주문번호"] not in rec["ce_seen"] else 0
                        rec["ce_owner_del"] += int(r["사장배달비분담"]) if r["주문번호"] not in rec["ce_seen"] else 0
                        rec["ce_seen"].add(r["주문번호"])
                    rec["del_cost"] += int(r["원가합계"])

    # 출력
    path = OUT / "daily_summary.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "날짜", "요일", "영업여부", "특이사항",
            "홀_주문수", "홀_매출",
            "배민_주문수", "배민_매출", "배민_앱수수료", "배민_PG수수료", "배민_광고수수료", "배민_사장배달비",
            "쿠팡이츠_주문수", "쿠팡이츠_매출", "쿠팡이츠_앱수수료", "쿠팡이츠_PG수수료", "쿠팡이츠_사장배달비",
            "총매출", "총원가", "정산순매출", "마진추정",
            "코스_매출", "주류_매출",
        ])

        all_days = []
        d = date(2026, 3, 1)
        while d <= date(2026, 4, 30):
            all_days.append(d)
            d += timedelta(days=1)

        for d in all_days:
            if d not in summary:
                # 휴무일
                w.writerow([
                    d.isoformat(), WEEKDAY_LABEL[d.weekday()], "휴무", _note(d),
                    0, 0,
                    0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0,
                    0, 0, 0, 0,
                    0, 0,
                ])
                continue

            r = summary[d]
            total_sales = r["pos_sales"] + r["bm_sales"] + r["ce_sales"]
            total_cost = r["pos_cost"] + r["del_cost"]
            net_rev = (
                r["pos_sales"]
                + (r["bm_sales"] - r["bm_app_fee"] - r["bm_pg_fee"] - r["bm_ad_fee"] - r["bm_owner_del"])
                + (r["ce_sales"] - r["ce_app_fee"] - r["ce_pg_fee"] - r["ce_owner_del"])
            )
            margin = net_rev - total_cost

            w.writerow([
                d.isoformat(), WEEKDAY_LABEL[d.weekday()], "영업", _note(d),
                len(r["pos_orders"]), r["pos_sales"],
                len(r["bm_orders"]), r["bm_sales"], r["bm_app_fee"], r["bm_pg_fee"], r["bm_ad_fee"], r["bm_owner_del"],
                len(r["ce_orders"]), r["ce_sales"], r["ce_app_fee"], r["ce_pg_fee"], r["ce_owner_del"],
                total_sales, total_cost, net_rev, margin,
                r["코스_매출"], r["주류_매출"],
            ])

    print(f"[OK] daily_summary.csv: 61 days")


def _new_daily(d: date):
    return {
        "pos_orders": set(), "pos_sales": 0, "pos_cost": 0,
        "bm_orders": set(), "bm_sales": 0, "bm_app_fee": 0, "bm_pg_fee": 0, "bm_ad_fee": 0, "bm_owner_del": 0, "bm_seen": set(),
        "ce_orders": set(), "ce_sales": 0, "ce_app_fee": 0, "ce_pg_fee": 0, "ce_owner_del": 0, "ce_seen": set(),
        "del_cost": 0,
        "코스_매출": 0, "주류_매출": 0,
    }


def _note(d: date) -> str:
    notes = {
        date(2026, 3, 1): "삼일절 (공휴일)",
        date(2026, 3, 2): "삼일절 대체 (공휴일)",
        date(2026, 4, 12): "인스타 릴스 바이럴",
        date(2026, 4, 25): "폭우 (배달 수요 급감 가정)",
        date(2026, 4, 30): "부처님오신날 (공휴일)",
    }
    if is_closed(d):
        return "정기휴무 (월)"
    return notes.get(d, "")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    write_menu_master()
    write_pos_sales(3)
    write_pos_sales(4)
    write_delivery_sales(3)
    write_delivery_sales(4)
    build_daily_summary()
    print("\n[DONE] All files in", OUT)
