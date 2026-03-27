"""
HFK (HBR Forum Korea) 샘플 데이터 생성 스크립트
저장 위치: /Users/rhim/Projects/do-better-workspace/50-resources/sample-data/hfk/
"""

import csv
import random
import os
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

random.seed(42)

# 기본 데이터
TEAMS = ["AI부사수", "마케팅디깅", "고급파전략", "저스트", "리더십랩", "북클럽클래식", "커리어피벗", "영어토론"]
RANKS = ["사원", "대리", "과장", "차장", "부장", "임원"]
INDUSTRIES = ["IT", "금융", "컨설팅", "제조", "유통", "의료", "미디어", "교육", "스타트업", "공공"]
CHANNELS = ["인스타", "지인추천", "롱블랙기사", "구글검색", "유튜브", "오픈채팅방", "기타"]

KOREAN_SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "전", "홍", "고", "문", "양", "손", "배", "백", "허", "유", "남", "심", "노", "하", "곽", "성", "차", "주", "우", "구", "민", "나", "진", "지", "엄", "채", "원", "천", "방", "공", "현"]
KOREAN_GIVEN = ["민준", "서준", "예준", "도윤", "시우", "주원", "하준", "지호", "지후", "준서", "준우", "현우", "도현", "지훈", "건우", "우진", "선우", "서진", "민재", "현준", "지원", "수빈", "수아", "지아", "서연", "서윤", "지윤", "하은", "하윤", "민서", "지유", "윤서", "채원", "수연", "아인", "다은", "유나", "예린", "지은", "소율", "예은", "나연", "가은", "다현", "소연", "보미", "세연", "혜원", "은서", "태양", "성민", "재혁", "병준", "동현", "태현", "승현", "준혁", "정민", "성준", "재원", "민호", "진호", "태준", "우혁", "재민", "성호", "동준", "민혁", "진우", "수호", "영민", "재현", "태호", "상민", "진혁", "영준", "상현", "재준"]

def gen_name(seed_extra=0):
    s = random.choice(KOREAN_SURNAMES)
    g = random.choice(KOREAN_GIVEN)
    return s + g

def random_date(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime("%Y-%m-%d")


# ─────────────────────────────────────────────
# 데이터 1: hfk_members_2026spring.csv
# ─────────────────────────────────────────────
def gen_members():
    total = 152
    new_count = 42
    renew_count = 110

    # 이름 풀 생성 (유니크)
    names = []
    used_names = set()
    while len(names) < total + 20:
        n = gen_name()
        if n not in used_names:
            used_names.add(n)
            names.append(n)

    # 부부 쌍 설정 (2쌍)
    couple_pairs = [
        (names[10], names[11]),
        (names[25], names[26]),
    ]

    # 장학금 멤버 인덱스 5개
    scholarship_indices = random.sample(range(total), 5)
    # 얼리버드 인덱스 (약 25% = 38명)
    earlybird_indices = set(random.sample(range(total), 38))
    # 장학금은 얼리버드에서 제외
    earlybird_indices -= set(scholarship_indices)

    # 1지망 가중치: AI부사수 40%+
    def pick_first_choice():
        r = random.random()
        if r < 0.40:
            return "AI부사수"
        else:
            return random.choice(TEAMS)

    # 배정 팀 (각 팀 약 19명씩)
    team_slots = []
    for t in TEAMS:
        team_slots.extend([t] * 19)
    team_slots = team_slots[:total]
    random.shuffle(team_slots)

    rows = []
    couple_map = {}
    for p1, p2 in couple_pairs:
        couple_map[p1] = p2
        couple_map[p2] = p1

    # 전설의 멤버 (8시즌 연속)
    legend_index = random.randint(new_count + 5, total - 5)

    referrers_pool = names[:total]

    for i in range(total):
        member_id = f"HFK-2026S-{i+1:03d}"

        # 강동원 이스터에그
        if i == 41:  # 042번째 = index 41
            name = "강동원"
        else:
            name = names[i]

        is_new = i < new_count
        member_type = "신규" if is_new else "재등록"

        if is_new:
            renew_count_val = 0
        elif i == legend_index:
            renew_count_val = 8
        else:
            renew_count_val = random.randint(1, 6)

        team = team_slots[i]
        first_choice = pick_first_choice()

        rank = random.choices(RANKS, weights=[15, 25, 25, 15, 12, 8])[0]
        industry = random.choice(INDUSTRIES)

        if i in scholarship_indices:
            payment = 270000
        elif i in earlybird_indices:
            payment = 486000
        else:
            payment = 540000

        payment_method = random.choices(["카드", "계좌이체"], weights=[70, 30])[0]

        # 추천인 (부부 쌍 우선)
        if name in couple_map:
            referrer = couple_map[name]
            has_referrer = "있음"
        elif not is_new and random.random() < 0.3:
            referrer = random.choice(referrers_pool[:total])
            if referrer == name:
                referrer = referrers_pool[(referrers_pool.index(name) + 1) % total]
            has_referrer = "있음"
        elif is_new and random.random() < 0.4:
            referrer = random.choice(referrers_pool[:new_count + 20])
            has_referrer = "있음"
        else:
            referrer = ""
            has_referrer = "없음"

        channel = random.choices(
            CHANNELS,
            weights=[20, 30, 10, 10, 10, 10, 10]
        )[0]

        reg_date = random_date("2026-02-01", "2026-02-28")

        rows.append({
            "멤버ID": member_id,
            "이름": name,
            "등록일": reg_date,
            "유형": member_type,
            "재등록횟수": renew_count_val,
            "배정팀": team,
            "1지망팀": first_choice,
            "직급": rank,
            "업종": industry,
            "결제금액": payment,
            "결제수단": payment_method,
            "추천인": referrer if has_referrer == "있음" else "",
            "추천인유무": has_referrer,
            "가입경로": channel,
        })

    # 전설의 멤버 표시 확인
    rows[legend_index]["재등록횟수"] = 8

    out_path = os.path.join(OUTPUT_DIR, "hfk_members_2026spring.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[완료] {out_path} ({len(rows)}행)")
    return rows


# ─────────────────────────────────────────────
# 데이터 2: hfk_feedback_2025winter.csv
# ─────────────────────────────────────────────
GOOD_COMMENTS = [
    "정동 뷰가 미쳤음. 덕수궁 석양 보면서 HBR 읽는 맛",
    "재윤님이 갑자기 Claude한테 '우리 안 한거 뭐야' 물어봤을때 다같이 웃었음",
    "슬기님 슬랙 공지에 오타가 줄었어요 감동",
    "팀원들이랑 밥 먹으러 가는게 이 커뮤니티의 핵심",
    "북클럽클래식 팀장님이 요약을 너무 잘 해주셔서 책 안 읽어도 됨 ㅋㅋ",
    "네트워킹 퀄리티가 다름. 다들 진짜 일 잘하는 사람들",
    "파트너 언니 덕분에 이직 성공했습니다",
    "오프닝데이 에너지 진짜 좋았음",
    "클로징데이 발표 보면서 내가 뭘 배웠는지 정리됨",
    "도쿄 필드트립 평생 잊을 수 없음",
    "AI팀인데 GPT vs Claude 논쟁이 3시간 걸린 날이 있었음",
    "매 시즌 새로운 사람 만나는 게 최고 자산",
    "고급파전략 팀 케이스스터디 퀄이 진짜 높음",
    "커리어피벗 덕분에 이직 방향 잡았음",
    "슬랙 채널이 살아있어서 좋음. 죽은 커뮤니티가 아님",
    "영어토론팀 덕분에 말문이 트임",
    "주 2회 미팅인데 부담 안 됨. 이 밸런스가 딱임",
    "같은 고민을 가진 사람들이 있다는 것만으로도 충분",
    "마케팅디깅 팀 실무 인사이트 갖고 가는 게 많음",
    "차박캠핑 새벽에 다같이 라면 먹은 거 명장면",
    "차박에서 재윤님이 텐트 못 치는거 봄 ㅋㅋ",
    "정동 오아시스 공간 자체가 선물",
    "부부멤버가 팀 미팅에서 말다툼한 건 좀 ㅋㅋ",
]

BAD_COMMENTS = [
    "54만원인데 커피는 왜 자판기...",
    "파트너 승격 기준이 뭔지 아직도 모르겠음",
    "시즌 중반 넘어가면 참여율이 뚝 떨어짐",
    "슬랙 알림이 너무 많아서 끄게 됨",
    "팀 배정이 1지망 반영 안 될 때 실망스러움",
    "오프라인 행사 날짜가 직장인한테 좀 빡셈",
    "54만원 가성비를 증명하려면 콘텐츠 더 필요",
    "온보딩이 좀 더 체계적이면 좋겠음 (신규 멤버 입장)",
    "팀별 온도차가 있음. 팀 운에 좌우되는 부분 있음",
    "겨울시즌은 연말이라 집중하기 어려운 시기",
    "클로징데이 준비 시간이 너무 촉박했음",
    "피드백이 실제로 반영되는지 모르겠음",
    "해외 필드트립 추가 비용이 부담스러움",
    "앱이 없어서 슬랙 의존도가 너무 높음",
    "팀장 역량에 따라 시즌 퀄리티가 많이 갈림",
    "번개모임이 서울 중심이라 외곽 멤버는 참여 어려움",
    "주차 공간이 없어서 대중교통 필수인 점 아쉬움",
]

def gen_feedback():
    total = 165
    rows = []

    for i in range(total):
        fb_id = f"FB-2025W-{i+1:03d}"
        member_id = f"HFK-25W-{random.randint(1, 168):03d}"
        submit_date = random_date("2026-02-15", "2026-02-28")
        team = random.choice(TEAMS)

        overall = max(1, min(5, round(random.gauss(4.1, 0.8))))
        team_sat = max(1, min(5, round(random.gauss(4.0, 0.9))))
        event_sat = max(1, min(5, round(random.gauss(3.9, 0.9))))
        space_sat = max(1, min(5, round(random.gauss(4.3, 0.7))))
        network_sat = max(1, min(5, round(random.gauss(4.0, 0.8))))
        value_sat = max(1, min(5, round(random.gauss(3.4, 0.9))))  # 가성비는 낮게

        renew_intent_opts = ["매우높음", "높음", "보통", "낮음", "매우낮음"]
        renew_weights = [30, 35, 20, 10, 5]
        renew_intent = random.choices(renew_intent_opts, weights=renew_weights)[0]

        nps = max(0, min(10, int(random.gauss(7.2, 1.8))))

        good = random.choice(GOOD_COMMENTS)
        bad = random.choice(BAD_COMMENTS)
        next_team = random.choices(TEAMS + ["상관없음"], weights=[5]*8 + [36])[0]

        rows.append({
            "피드백ID": fb_id,
            "멤버ID": member_id,
            "제출일": submit_date,
            "소속팀": team,
            "전체만족도": overall,
            "팀활동만족도": team_sat,
            "이벤트만족도": event_sat,
            "공간만족도": space_sat,
            "네트워킹만족도": network_sat,
            "가성비만족도": value_sat,
            "재등록의향": renew_intent,
            "추천의향NPS": nps,
            "좋았던점": good,
            "아쉬운점": bad,
            "다음시즌희망팀": next_team,
        })

    out_path = os.path.join(OUTPUT_DIR, "hfk_feedback_2025winter.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[완료] {out_path} ({len(rows)}행)")


# ─────────────────────────────────────────────
# 데이터 3: hfk_events_2025winter.csv
# ─────────────────────────────────────────────
def gen_events():
    rows = [
        {
            "이벤트ID": "EVT-2025W-01",
            "이벤트명": "오프닝데이",
            "날짜": "2025-12-06",
            "유형": "정기",
            "장소": "정동오아시스",
            "정원": 168,
            "신청수": 162,
            "참석수": 155,
            "노쇼수": 7,
            "참가비": 0,
            "만족도평균": 4.5,
            "비고": "시즌 킥오프. 팀 배정 발표"
        },
        {
            "이벤트ID": "EVT-2025W-02",
            "이벤트명": "네트워킹나이트1",
            "날짜": "2025-12-20",
            "유형": "정기",
            "장소": "정동오아시스",
            "정원": 80,
            "신청수": 95,
            "참석수": 78,
            "노쇼수": 17,
            "참가비": 0,
            "만족도평균": 4.2,
            "비고": "연말 분위기로 참여 높음"
        },
        {
            "이벤트ID": "EVT-2025W-03",
            "이벤트명": "번개모임_을지로노가리",
            "날짜": "2025-12-27",
            "유형": "번개",
            "장소": "을지로",
            "정원": 20,
            "신청수": 34,
            "참석수": 19,
            "노쇼수": 15,
            "참가비": 15000,
            "만족도평균": 4.9,
            "비고": "만족도 최고. 노가리+맥주 조합"
        },
        {
            "이벤트ID": "EVT-2025W-04",
            "이벤트명": "차박캠핑",
            "날짜": "2026-01-10",
            "유형": "특별",
            "장소": "양평",
            "정원": 40,
            "신청수": 52,
            "참석수": 40,
            "노쇼수": 0,
            "참가비": 30000,
            "만족도평균": 4.7,
            "비고": "노쇼 0명. 텐트 때문에 다들 긴장. 재윤님 텐트 설치 실패 전설"
        },
        {
            "이벤트ID": "EVT-2025W-05",
            "이벤트명": "번개모임_강남커피",
            "날짜": "2026-01-15",
            "유형": "번개",
            "장소": "강남",
            "정원": 15,
            "신청수": 22,
            "참석수": 13,
            "노쇼수": 9,
            "참가비": 0,
            "만족도평균": 3.8,
            "비고": "주중 저녁. 직장인 노쇼 多"
        },
        {
            "이벤트ID": "EVT-2025W-06",
            "이벤트명": "도쿄필드트립",
            "날짜": "2026-01-23",
            "유형": "특별",
            "장소": "도쿄",
            "정원": 30,
            "신청수": 91,
            "참석수": 29,
            "노쇼수": 1,
            "참가비": 450000,
            "만족도평균": 4.8,
            "비고": "신청수 정원의 3배. 로또 추첨으로 선발"
        },
        {
            "이벤트ID": "EVT-2025W-07",
            "이벤트명": "네트워킹나이트2",
            "날짜": "2026-01-31",
            "유형": "정기",
            "장소": "정동오아시스",
            "정원": 80,
            "신청수": 74,
            "참석수": 68,
            "노쇼수": 6,
            "참가비": 0,
            "만족도평균": 4.1,
            "비고": ""
        },
        {
            "이벤트ID": "EVT-2025W-08",
            "이벤트명": "번개모임_홍대",
            "날짜": "2026-02-07",
            "유형": "번개",
            "장소": "홍대",
            "정원": 25,
            "신청수": 31,
            "참석수": 22,
            "노쇼수": 9,
            "참가비": 10000,
            "만족도평균": 4.0,
            "비고": "AI팀 자체 번개"
        },
        {
            "이벤트ID": "EVT-2025W-09",
            "이벤트명": "번개모임_을지로2차",
            "날짜": "2026-02-14",
            "유형": "번개",
            "장소": "을지로",
            "정원": 25,
            "신청수": 38,
            "참석수": 24,
            "노쇼수": 14,
            "참가비": 15000,
            "만족도평균": 4.6,
            "비고": "발렌타인데이 번개. 부부멤버 동반 참석"
        },
        {
            "이벤트ID": "EVT-2025W-10",
            "이벤트명": "클로징데이",
            "날짜": "2026-02-22",
            "유형": "정기",
            "장소": "정동오아시스",
            "정원": 168,
            "신청수": 148,
            "참석수": 138,
            "노쇼수": 10,
            "참가비": 0,
            "만족도평균": 4.4,
            "비고": "시즌 마무리. 팀별 발표 + 파트너 승격 발표"
        },
    ]

    # 추가 번개 모임 랜덤 생성 (~20개)
    venues = ["강남", "홍대", "을지로", "정동오아시스", "성수", "합정", "마포"]
    event_names_extra = [
        "번개모임_AI독서모임", "번개모임_북클럽", "번개모임_커리어토크",
        "번개모임_스터디", "번개모임_점심런치", "번개모임_저녁회식",
        "번개모임_마케팅세미나", "번개모임_신규환영", "번개모임_리더십토론",
        "번개모임_영어스터디", "번개모임_사이드프로젝트", "번개모임_파트너모임",
        "번개모임_연말파티", "번개모임_신년회", "번개모임_팀장모임",
        "번개모임_러닝크루", "번개모임_전시관람", "번개모임_기업탐방",
        "번개모임_멘토링", "번개모임_투자스터디",
    ]

    dates_range = [
        "2025-12-13", "2025-12-19", "2025-12-28",
        "2026-01-04", "2026-01-08", "2026-01-17", "2026-01-24",
        "2026-02-01", "2026-02-05", "2026-02-08", "2026-02-11",
        "2026-02-13", "2026-02-15", "2026-02-17", "2026-02-18",
        "2026-02-19", "2026-02-20", "2026-02-21",
        "2025-12-07", "2025-12-14",
    ]

    for j, (ename, edate) in enumerate(zip(event_names_extra, dates_range)):
        capacity = random.choice([10, 12, 15, 20, 25])
        applications = capacity + random.randint(-3, 10)
        applications = max(applications, int(capacity * 0.7))
        attended = min(applications, capacity) - random.randint(0, 3)
        noshow = applications - attended if applications > attended else 0
        satisfaction = round(random.uniform(3.5, 4.8), 1)

        rows.append({
            "이벤트ID": f"EVT-2025W-{11 + j:02d}",
            "이벤트명": ename,
            "날짜": edate,
            "유형": "번개",
            "장소": random.choice(venues),
            "정원": capacity,
            "신청수": applications,
            "참석수": attended,
            "노쇼수": noshow,
            "참가비": random.choice([0, 0, 10000, 15000, 20000]),
            "만족도평균": satisfaction,
            "비고": "",
        })

    # 날짜순 정렬
    rows.sort(key=lambda x: x["날짜"])

    out_path = os.path.join(OUTPUT_DIR, "hfk_events_2025winter.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[완료] {out_path} ({len(rows)}행)")


# ─────────────────────────────────────────────
# 데이터 4: hfk_revenue_seasons.csv
# ─────────────────────────────────────────────
def gen_revenue():
    seasons = [
        {"시즌": "2024가을", "시즌코드": "24F", "등록수": 145, "신규율": 0.28},
        {"시즌": "2024겨울", "시즌코드": "24W", "등록수": 158, "신규율": 0.26},
        {"시즌": "2025봄",   "시즌코드": "25S", "등록수": 172, "신규율": 0.29},
        {"시즌": "2025여름", "시즌코드": "25U", "등록수": 187, "신규율": 0.27},
        {"시즌": "2025가을", "시즌코드": "25F", "등록수": 203, "신규율": 0.25},
        {"시즌": "2025겨울", "시즌코드": "25W", "등록수": 168, "신규율": 0.24},
        {"시즌": "2026봄",   "시즌코드": "26S", "등록수": 152, "신규율": 0.28},
    ]

    # 해외 필드트립 있는 시즌 (이벤트비 높음): 25가을(교토), 25겨울(도쿄)
    overseas_seasons = {"25F", "25W"}

    prev_count = 140  # 24가을 직전 시즌 기준
    rows = []
    for s in seasons:
        n = s["등록수"]
        new_n = round(n * s["신규율"])
        renew_n = n - new_n

        if s["시즌코드"] == "24F":
            renew_rate = 0.0
        else:
            renew_rate = round(renew_n / prev_count * 100, 1)

        earlybird_n = round(n * random.uniform(0.20, 0.28))
        scholarship_n = random.randint(3, 5)
        refund_n = random.randint(0, 3)

        base_revenue = (
            (n - earlybird_n - scholarship_n) * 540000
            + earlybird_n * 486000
            + scholarship_n * 270000
        )
        net_revenue = base_revenue - refund_n * 540000

        space_cost = 12_000_000
        event_cost = random.randint(14_000_000, 18_000_000) if s["시즌코드"] in overseas_seasons else random.randint(5_000_000, 8_000_000)
        ops_cost = random.randint(7_500_000, 8_500_000)
        total_cost = space_cost + event_cost + ops_cost
        op_profit = net_revenue - total_cost

        rows.append({
            "시즌": s["시즌"],
            "시즌코드": s["시즌코드"],
            "등록수": n,
            "신규수": new_n,
            "재등록수": renew_n,
            "재등록률(%)": renew_rate if s["시즌코드"] != "24F" else "-",
            "총매출": base_revenue,
            "얼리버드수": earlybird_n,
            "장학금수": scholarship_n,
            "환불수": refund_n,
            "순매출": net_revenue,
            "공간비": space_cost,
            "이벤트비": event_cost,
            "운영비": ops_cost,
            "영업이익": op_profit,
        })

        prev_count = n

    out_path = os.path.join(OUTPUT_DIR, "hfk_revenue_seasons.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[완료] {out_path} ({len(rows)}행)")


if __name__ == "__main__":
    print("HFK 샘플 데이터 생성 시작...\n")
    gen_members()
    gen_feedback()
    gen_events()
    gen_revenue()
    print("\n전체 완료.")
