#!/usr/bin/env python3
"""무신사/29CM 마케팅 시연용 가상 데이터 생성 스크립트"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 공통 상수
# ============================================================

BRANDS = ["무신사", "29CM"]
PLATFORMS_SNS = ["인스타그램", "유튜브", "틱톡"]
CATEGORIES = ["아우터", "데님", "니트/스웨터", "셔츠/블라우스", "스니커즈", "부츠", "가방", "액세서리", "뷰티", "라이프스타일"]

# 가상 인플루언서 이름 풀
INFLUENCER_NAMES = {
    "메가": ["스타일킹 지호", "패션유니버스", "루나스타일", "핏마스터 현우", "트렌드퀸 소연",
             "옷잘입는남자 준서", "패션위크 다영", "OOTD 민재"],
    "매크로": ["데일리룩 서연", "스트릿바이브", "미니멀리스트 하은", "캐주얼킹 도윤", "코디장인 유나",
              "레이어드 마스터", "빈티지무드 재현", "클린핏 소율", "어반스타일 시우", "모던룩 지안",
              "감성코디 예린", "프렙룩 태민", "시크바이브 하린", "놈코어 정우", "믹스매치 수아"],
    "마이크로": [f"마이크로_{i:03d}" for i in range(1, 151)],
    "나노": [f"나노_{i:03d}" for i in range(1, 101)],
}

CONTENT_TYPES_INF = ["릴스", "피드", "스토리", "쇼츠", "라이브"]
CONTENT_TYPES_SNS = ["릴스", "피드", "카루셀", "스토리", "쇼츠"]
CONTENT_THEMES = ["룩북", "상품소개", "이벤트", "브랜드스토리", "UGC리포스트", "에디토리얼", "PT컬렉션"]

CHANNELS_CAMPAIGN = ["인스타그램", "유튜브", "네이버", "카카오", "앱푸시", "CRM", "틱톡"]
CAMPAIGN_TYPES = ["브랜딩", "퍼포먼스", "리타겟팅", "CRM"]
TARGET_SEGMENTS = ["MZ남성", "2030여성", "VIP", "신규유입", "이탈방지", "브랜드관심"]

MEDIA_PLATFORMS = ["메타(인스타/FB)", "구글", "네이버SA", "카카오모먼트", "틱톡", "유튜브"]
AD_TYPES = ["디스플레이", "검색광고", "동영상", "쇼핑광고", "리타겟팅"]
AUDIENCES = ["리타겟팅", "LAL(유사타깃)", "관심사", "브로드", "CRM시드"]

TEAM_MEMBERS = ["김지현", "박서연", "이준혁", "최유진", "정하늘", "윤세영", "한도경", "송민아"]

ACCOUNTS_SNS = {"무신사": "@musinsa_official", "29CM": "@29cm_official"}

# ============================================================
# 1. 인플루언서 데이터 생성
# ============================================================

def generate_influencer_data():
    """musinsa_influencer_2602.csv - ~300행"""
    rows = []
    idx = 0

    # 등급별 설정: (팔로워 범위, engagement rate 범위, 비용 범위, 전환율 범위)
    tier_config = {
        "메가":   {"followers": (1_000_000, 5_000_000), "er": (0.01, 0.03), "cost": (15_000_000, 35_000_000), "cvr": (0.008, 0.018), "link_ctr": (0.005, 0.015)},
        "매크로": {"followers": (100_000, 999_999),     "er": (0.03, 0.06), "cost": (3_000_000, 10_000_000),  "cvr": (0.02, 0.045),  "link_ctr": (0.01, 0.025)},
        "마이크로": {"followers": (10_000, 99_999),     "er": (0.05, 0.12), "cost": (300_000, 1_500_000),     "cvr": (0.06, 0.12),   "link_ctr": (0.015, 0.04)},
        "나노":   {"followers": (1_000, 9_999),         "er": (0.08, 0.18), "cost": (50_000, 300_000),        "cvr": (0.07, 0.15),   "link_ctr": (0.02, 0.05)},
    }

    # 등급별 인원수
    tier_counts = {"메가": 8, "매크로": 15, "마이크로": 150, "나노": 100}

    for tier, count in tier_counts.items():
        cfg = tier_config[tier]
        names = INFLUENCER_NAMES[tier][:count]

        for name in names:
            # 한 인플루언서가 여러 콘텐츠 게시 가능 (메가 3-5, 매크로 2-3, 마이크로 1-2, 나노 1)
            if tier == "메가":
                num_posts = random.randint(3, 5)
            elif tier == "매크로":
                num_posts = random.randint(2, 3)
            elif tier == "마이크로":
                num_posts = random.randint(1, 2)
            else:
                num_posts = 1

            followers = random.randint(*cfg["followers"])
            platform = random.choice(PLATFORMS_SNS)

            # 틱톡 engagement rate 보너스
            er_boost = 1.3 if platform == "틱톡" else 1.0

            for _ in range(num_posts):
                idx += 1
                er = random.uniform(*cfg["er"]) * er_boost
                cost = random.randint(*cfg["cost"])
                impressions = int(followers * random.uniform(0.3, 1.5))
                likes = int(impressions * er * random.uniform(0.5, 0.7))
                comments = int(likes * random.uniform(0.05, 0.15))
                saves = int(likes * random.uniform(0.1, 0.3))
                shares = int(likes * random.uniform(0.03, 0.08))
                link_clicks = int(impressions * random.uniform(*cfg["link_ctr"]))
                cvr = random.uniform(*cfg["cvr"])
                conversions = max(1, int(link_clicks * cvr))
                # 마이크로/나노: 타깃 정합성 높아 객단가도 높음
                if tier == "나노":
                    avg_order = random.randint(95_000, 190_000)
                elif tier == "마이크로":
                    avg_order = random.randint(85_000, 170_000)
                elif tier == "매크로":
                    avg_order = random.randint(65_000, 130_000)
                else:  # 메가: 노출은 크지만 구매 의향 낮은 관객 많음
                    avg_order = random.randint(45_000, 95_000)
                revenue = conversions * avg_order

                brand = random.choice(BRANDS)
                # 29CM 인플루언서: 저장수 높게 (큐레이션 성격)
                if brand == "29CM":
                    saves = int(saves * 1.8)

                content_type = random.choice(CONTENT_TYPES_INF)
                if platform == "유튜브":
                    content_type = random.choice(["쇼츠", "라이브", "피드"])
                elif platform == "틱톡":
                    content_type = random.choice(["쇼츠", "라이브"])

                post_day = random.randint(1, 28)
                post_date = f"2026-02-{post_day:02d}"

                rows.append({
                    "협업ID": f"INF-2602-{idx:03d}",
                    "인플루언서명": name,
                    "플랫폼": platform,
                    "팔로워수": followers,
                    "등급": tier,
                    "콘텐츠유형": content_type,
                    "게시일": post_date,
                    "노출수": impressions,
                    "좋아요": likes,
                    "댓글수": comments,
                    "저장수": saves,
                    "공유수": shares,
                    "링크클릭": link_clicks,
                    "전환수": conversions,
                    "비용": cost,
                    "매출기여": revenue,
                    "카테고리": random.choice(CATEGORIES),
                    "브랜드": brand,
                })

    random.shuffle(rows)
    filepath = os.path.join(OUTPUT_DIR, "musinsa_influencer_2602.csv")
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] {filepath} ({len(rows)}행)")
    return len(rows)


# ============================================================
# 2. 캠페인 성과 데이터 생성
# ============================================================

def generate_campaign_data(month=2, year=2026):
    """musinsa_campaign_performance_26XX.csv"""
    rows = []
    idx = 0

    mm = f"{month:02d}"
    days_in_month = 28 if month == 2 else 31

    # 설 연휴 효과 (1월)
    is_jan = (month == 1)

    # 캠페인 유형별 성과 프로필
    type_profiles = {
        "브랜딩":   {"ctr": (0.005, 0.015), "cvr": (0.005, 0.015), "roas": (1.5, 3.0)},
        "퍼포먼스": {"ctr": (0.015, 0.035), "cvr": (0.02, 0.05),   "roas": (3.0, 6.0)},
        "리타겟팅": {"ctr": (0.03, 0.06),   "cvr": (0.05, 0.10),   "roas": (8.0, 15.0)},
        "CRM":      {"ctr": (0.04, 0.08),   "cvr": (0.06, 0.12),   "roas": (5.0, 10.0)},
    }

    # 채널별 가중치
    channel_weights = {
        "인스타그램": 25, "유튜브": 10, "네이버": 20, "카카오": 15,
        "앱푸시": 12, "CRM": 8, "틱톡": 10,
    }

    target_rows = 2500 if month == 2 else 2000
    campaigns_per_type = target_rows // (len(CAMPAIGN_TYPES) * len(CHANNELS_CAMPAIGN))

    for camp_type in CAMPAIGN_TYPES:
        prof = type_profiles[camp_type]
        for channel in CHANNELS_CAMPAIGN:
            n = max(5, campaigns_per_type + random.randint(-3, 3))
            if is_jan:
                n = int(n * 0.8)  # 1월은 설 연휴로 캠페인 수 줄어듬

            for _ in range(n):
                idx += 1
                start_day = random.randint(1, max(1, days_in_month - 7))
                duration = random.randint(1, 14)
                end_day = min(days_in_month, start_day + duration)

                start_date = f"{year}-{mm}-{start_day:02d}"
                end_date = f"{year}-{mm}-{end_day:02d}"

                brand = random.choices(BRANDS, weights=[60, 40])[0]
                # 29CM CRM 전환율 보너스
                cvr_boost = 1.5 if (brand == "29CM" and camp_type == "CRM") else 1.0

                budget = random.randint(500_000, 30_000_000)
                if is_jan and random.random() < 0.3:  # 설 연휴 예산 축소
                    budget = int(budget * 0.6)

                impressions = int(budget / random.uniform(3, 15))  # CPM 3~15원
                ctr = random.uniform(*prof["ctr"])
                clicks = max(1, int(impressions * ctr))
                cvr = random.uniform(*prof["cvr"]) * cvr_boost
                conversions = max(0, int(clicks * cvr))
                roas = random.uniform(*prof["roas"])
                revenue = int(budget * roas)

                # 주말 CTR 보너스
                start_dt = datetime(year, month, start_day)
                if start_dt.weekday() >= 5:
                    clicks = int(clicks * 1.2)
                    conversions = int(conversions * 1.15)

                camp_name = f"{mm}월_{brand}_{channel}_{camp_type}_{idx}"

                rows.append({
                    "캠페인ID": f"MKT-{year % 100}{mm}-{idx:04d}",
                    "캠페인명": camp_name,
                    "시작일": start_date,
                    "종료일": end_date,
                    "채널": channel,
                    "캠페인유형": camp_type,
                    "타깃세그먼트": random.choice(TARGET_SEGMENTS),
                    "노출수": impressions,
                    "클릭수": clicks,
                    "전환수": conversions,
                    "집행비용": budget,
                    "매출기여": revenue,
                    "브랜드": brand,
                    "담당자": random.choice(TEAM_MEMBERS),
                })

    random.shuffle(rows)
    suffix = f"26{mm}"
    filepath = os.path.join(OUTPUT_DIR, f"musinsa_campaign_performance_{suffix}.csv")
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] {filepath} ({len(rows)}행)")
    return len(rows)


# ============================================================
# 3. 매체비 집행 데이터 생성
# ============================================================

def generate_media_spend():
    """musinsa_media_spend_2602.csv - ~200행"""
    rows = []
    idx = 0

    # 매체별 성과 프로필
    media_profiles = {
        "메타(인스타/FB)": {"cpm": (5, 12),  "ctr": (0.012, 0.025), "cvr": (0.02, 0.04),  "roas": (3.0, 5.5)},
        "구글":           {"cpm": (8, 18),   "ctr": (0.02, 0.04),   "cvr": (0.03, 0.05),  "roas": (3.5, 6.0)},
        "네이버SA":       {"cpm": (15, 35),  "ctr": (0.03, 0.06),   "cvr": (0.05, 0.09),  "roas": (6.0, 10.0)},
        "카카오모먼트":   {"cpm": (4, 10),   "ctr": (0.008, 0.018), "cvr": (0.015, 0.03), "roas": (2.5, 4.5)},
        "틱톡":           {"cpm": (3, 8),    "ctr": (0.015, 0.035), "cvr": (0.015, 0.035),"roas": (2.0, 4.0)},
        "유튜브":         {"cpm": (10, 25),  "ctr": (0.005, 0.015), "cvr": (0.01, 0.025), "roas": (2.0, 3.5)},
    }

    for day in range(1, 29):
        date = f"2026-02-{day:02d}"
        for media, prof in media_profiles.items():
            # 매체별 일 예산 (메타가 가장 큼)
            if media == "메타(인스타/FB)":
                daily_budget = random.randint(8_000_000, 15_000_000)
            elif media == "네이버SA":
                daily_budget = random.randint(5_000_000, 10_000_000)
            elif media == "구글":
                daily_budget = random.randint(3_000_000, 7_000_000)
            elif media == "카카오모먼트":
                daily_budget = random.randint(2_000_000, 5_000_000)
            elif media == "틱톡":
                # 틱톡: 월 초 낮다가 후반부 CPA 개선 추세
                base = random.randint(1_500_000, 4_000_000)
                daily_budget = base
                if day > 14:
                    prof = {**prof, "cvr": (0.025, 0.045), "roas": (3.0, 5.0)}  # 후반 개선
            else:  # 유튜브
                daily_budget = random.randint(2_000_000, 6_000_000)

            idx += 1
            cpm = random.uniform(*prof["cpm"])
            impressions = int(daily_budget / cpm)
            ctr = random.uniform(*prof["ctr"])
            clicks = max(1, int(impressions * ctr))
            cvr = random.uniform(*prof["cvr"])
            conversions = max(0, int(clicks * cvr))
            roas = random.uniform(*prof["roas"])
            revenue = int(daily_budget * roas)

            brand = random.choices(BRANDS, weights=[60, 40])[0]
            ad_type = random.choice(AD_TYPES)
            audience = random.choice(AUDIENCES)

            rows.append({
                "집행ID": f"MED-2602-{idx:03d}",
                "날짜": date,
                "매체": media,
                "광고유형": ad_type,
                "집행금액": daily_budget,
                "노출수": impressions,
                "클릭수": clicks,
                "전환수": conversions,
                "매출기여": revenue,
                "타깃오디언스": audience,
                "브랜드": brand,
            })

    filepath = os.path.join(OUTPUT_DIR, "musinsa_media_spend_2602.csv")
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] {filepath} ({len(rows)}행)")
    return len(rows)


# ============================================================
# 4. SNS 오가닉 데이터 생성
# ============================================================

def generate_sns_organic():
    """musinsa_sns_organic_2602.csv - ~400행"""
    rows = []
    idx = 0

    # 콘텐츠 유형별 성과 프로필 (도달 대비)
    type_profiles = {
        "릴스":   {"reach_mult": (3.0, 6.0), "like_rate": (0.04, 0.08), "save_rate": (0.01, 0.025), "comment_rate": (0.005, 0.015)},
        "피드":   {"reach_mult": (0.5, 1.2), "like_rate": (0.03, 0.06), "save_rate": (0.015, 0.035), "comment_rate": (0.003, 0.010)},
        "카루셀": {"reach_mult": (0.8, 1.8), "like_rate": (0.035, 0.07), "save_rate": (0.03, 0.06), "comment_rate": (0.004, 0.012)},
        "스토리": {"reach_mult": (0.3, 0.7), "like_rate": (0.01, 0.03), "save_rate": (0.002, 0.008), "comment_rate": (0.001, 0.005)},
        "쇼츠":   {"reach_mult": (2.5, 5.0), "like_rate": (0.05, 0.10), "save_rate": (0.008, 0.02), "comment_rate": (0.008, 0.020)},
    }

    # 계정별 기본 팔로워
    account_followers = {"@musinsa_official": 850_000, "@29cm_official": 320_000}

    for day in range(1, 29):
        date = f"2026-02-{day:02d}"
        for brand in BRANDS:
            account = ACCOUNTS_SNS[brand]
            base_followers = account_followers[account]

            # 하루 5~8개 콘텐츠
            daily_posts = random.randint(5, 8)
            for _ in range(daily_posts):
                idx += 1
                content_type = random.choices(
                    CONTENT_TYPES_SNS,
                    weights=[25, 25, 20, 20, 10],
                )[0]
                prof = type_profiles[content_type]

                channel = "인스타그램"
                if content_type == "쇼츠":
                    channel = random.choice(["유튜브", "틱톡"])

                reach = int(base_followers * random.uniform(*prof["reach_mult"]))
                likes = int(reach * random.uniform(*prof["like_rate"]))
                comments = int(reach * random.uniform(*prof["comment_rate"]))
                saves = int(reach * random.uniform(*prof["save_rate"]))
                shares = int(likes * random.uniform(0.02, 0.06))
                profile_visits = int(reach * random.uniform(0.005, 0.02))
                follower_delta = random.randint(-20, 150)

                # 29CM: engagement rate 높게 (작지만 충성)
                if brand == "29CM":
                    likes = int(likes * 1.4)
                    comments = int(comments * 1.6)
                    saves = int(saves * 1.5)
                    follower_delta = int(follower_delta * 0.7)  # 성장은 느림

                theme = random.choice(CONTENT_THEMES)
                # 29CM은 에디토리얼/PT컬렉션 비중 높게
                if brand == "29CM" and random.random() < 0.4:
                    theme = random.choice(["에디토리얼", "PT컬렉션", "브랜드스토리"])

                rows.append({
                    "게시물ID": f"SNS-2602-{idx:04d}",
                    "채널": channel,
                    "계정": account,
                    "게시일": date,
                    "콘텐츠유형": content_type,
                    "콘텐츠테마": theme,
                    "노출수": reach,
                    "좋아요": likes,
                    "댓글수": comments,
                    "저장수": saves,
                    "공유수": shares,
                    "프로필방문": profile_visits,
                    "팔로워증감": follower_delta,
                })

    filepath = os.path.join(OUTPUT_DIR, "musinsa_sns_organic_2602.csv")
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"  [OK] {filepath} ({len(rows)}행)")
    return len(rows)


# ============================================================
# 메인 실행
# ============================================================

if __name__ == "__main__":
    print("무신사/29CM 마케팅 시연 데이터 생성 시작\n")

    n1 = generate_influencer_data()
    print()
    n2 = generate_campaign_data(month=2, year=2026)
    print()
    n3 = generate_campaign_data(month=1, year=2026)
    print()
    n4 = generate_media_spend()
    print()
    n5 = generate_sns_organic()

    print(f"\n완료! 총 {n1 + n2 + n3 + n4 + n5}행 생성")
