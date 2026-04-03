"""
매드업 AX 데모 시나리오 더미데이터 생성기
- 6개 클라이언트 x 5개 매체 x 31일 = 캠페인 일별 성과
- 클라이언트 마스터 (계약조건, 수수료율, KPI 목표)
- 크리에이티브 소재별 성과
- 경쟁 에이전시 벤치마크
"""

import csv
import random
import math
from datetime import datetime, timedelta

random.seed(42)

# === 클라이언트 설정 ===
CLIENTS = {
    "글로우랩": {
        "industry": "뷰티/화장품",
        "monthly_budget": 180_000_000,  # 1.8억
        "commission_rate": 0.13,
        "kpi_primary": "ROAS",
        "kpi_target": 400,
        "media_mix": ["meta", "naver_sa", "naver_gfa", "kakao", "tiktok"],
        "account_manager": "김성연",
        "base_roas": {"meta": 380, "naver_sa": 520, "naver_gfa": 280, "kakao": 350, "tiktok": 310},
        "base_ctr": {"meta": 1.8, "naver_sa": 5.2, "naver_gfa": 0.18, "kakao": 0.35, "tiktok": 1.1},
        "base_cpc": {"meta": 850, "naver_sa": 3500, "naver_gfa": 420, "kakao": 550, "tiktok": 680},
        "base_cvr": {"meta": 2.8, "naver_sa": 4.5, "naver_gfa": 1.2, "kakao": 2.1, "tiktok": 1.5},
    },
    "어반핏": {
        "industry": "패션/의류",
        "monthly_budget": 120_000_000,
        "commission_rate": 0.15,
        "kpi_primary": "ROAS",
        "kpi_target": 350,
        "media_mix": ["meta", "google", "naver_sa", "kakao"],
        "account_manager": "박지은",
        "base_roas": {"meta": 340, "google": 290, "naver_sa": 450, "kakao": 320},
        "base_ctr": {"meta": 1.5, "google": 6.8, "naver_sa": 4.8, "kakao": 0.28},
        "base_cpc": {"meta": 1100, "google": 1800, "naver_sa": 4200, "kakao": 680},
        "base_cvr": {"meta": 2.1, "google": 3.2, "naver_sa": 3.8, "kakao": 1.6},
    },
    "프레시밀": {
        "industry": "F&B/밀키트",
        "monthly_budget": 75_000_000,
        "commission_rate": 0.15,
        "kpi_primary": "CPA",
        "kpi_target": 12000,
        "media_mix": ["meta", "naver_sa", "naver_gfa", "kakao"],
        "account_manager": "김성연",
        "base_roas": {"meta": 520, "naver_sa": 680, "naver_gfa": 350, "kakao": 480},
        "base_ctr": {"meta": 2.2, "naver_sa": 6.1, "naver_gfa": 0.22, "kakao": 0.42},
        "base_cpc": {"meta": 620, "naver_sa": 1800, "naver_gfa": 350, "kakao": 420},
        "base_cvr": {"meta": 3.5, "naver_sa": 5.8, "naver_gfa": 1.8, "kakao": 2.8},
    },
    "펫프렌즈": {
        "industry": "반려동물/이커머스",
        "monthly_budget": 250_000_000,
        "commission_rate": 0.12,
        "kpi_primary": "ROAS",
        "kpi_target": 450,
        "media_mix": ["meta", "google", "naver_sa", "naver_gfa", "kakao", "tiktok"],
        "account_manager": "이현수",
        "base_roas": {"meta": 420, "google": 380, "naver_sa": 580, "naver_gfa": 310, "kakao": 390, "tiktok": 280},
        "base_ctr": {"meta": 2.0, "google": 7.2, "naver_sa": 5.5, "naver_gfa": 0.20, "kakao": 0.32, "tiktok": 1.3},
        "base_cpc": {"meta": 780, "google": 1500, "naver_sa": 2800, "naver_gfa": 380, "kakao": 510, "tiktok": 620},
        "base_cvr": {"meta": 3.2, "google": 3.8, "naver_sa": 5.2, "naver_gfa": 1.5, "kakao": 2.4, "tiktok": 1.8},
    },
    "핀크레딧": {
        "industry": "금융/핀테크",
        "monthly_budget": 300_000_000,
        "commission_rate": 0.10,
        "kpi_primary": "CPA",
        "kpi_target": 25000,
        "media_mix": ["meta", "google", "naver_sa", "kakao"],
        "account_manager": "이현수",
        "base_roas": {"meta": 250, "google": 220, "naver_sa": 310, "kakao": 270},
        "base_ctr": {"meta": 1.1, "google": 5.5, "naver_sa": 3.8, "kakao": 0.22},
        "base_cpc": {"meta": 2200, "google": 5500, "naver_sa": 8500, "kakao": 1400},
        "base_cvr": {"meta": 1.5, "google": 2.1, "naver_sa": 2.8, "kakao": 1.2},
    },
    "딜리버리킹": {
        "industry": "O2O/배달",
        "monthly_budget": 95_000_000,
        "commission_rate": 0.14,
        "kpi_primary": "CPA",
        "kpi_target": 8000,
        "media_mix": ["meta", "google", "naver_gfa", "kakao", "tiktok"],
        "account_manager": "박지은",
        "base_roas": {"meta": 480, "google": 410, "naver_gfa": 320, "kakao": 440, "tiktok": 350},
        "base_ctr": {"meta": 2.5, "google": 6.5, "naver_gfa": 0.25, "kakao": 0.45, "tiktok": 1.6},
        "base_cpc": {"meta": 550, "google": 1200, "naver_gfa": 300, "kakao": 380, "tiktok": 480},
        "base_cvr": {"meta": 4.2, "google": 3.5, "naver_gfa": 2.0, "kakao": 3.2, "tiktok": 2.5},
    },
}

PLATFORM_LABELS = {
    "meta": "Meta",
    "google": "Google",
    "naver_sa": "Naver SA",
    "naver_gfa": "Naver GFA",
    "kakao": "Kakao",
    "tiktok": "TikTok",
}

CAMPAIGN_TYPE = {
    "meta": "DA",
    "google": "SA",
    "naver_sa": "SA",
    "naver_gfa": "DA",
    "kakao": "DA",
    "tiktok": "DA",
}

# 캠페인 이름 템플릿
CAMPAIGN_TEMPLATES = {
    "뷰티/화장품": ["봄신상_세럼", "화이트데이_선물세트", "베스트셀러_리타겟팅", "신규가입_프로모션"],
    "패션/의류": ["SS시즌_신상품", "화이트데이_커플룩", "봄아우터_프로모션", "앱설치_캠페인"],
    "F&B/밀키트": ["봄시즌_신메뉴", "화이트데이_디너세트", "정기구독_프로모션", "신규회원_할인"],
    "반려동물/이커머스": ["봄맞이_산책용품", "화이트데이_펫간식", "대용량_사료_프로모", "앱다운_이벤트"],
    "금융/핀테크": ["간편대출_유입", "신용카드_발급", "투자앱_설치", "이벤트_리타겟팅"],
    "O2O/배달": ["봄시즌_신규가맹점", "화이트데이_특별배달", "첫주문_할인", "앱설치_리워드"],
}

# 화이트데이(3/14) 전후 시즌 효과 - 날짜별 multiplier
def get_seasonal_multiplier(day, industry):
    """화이트데이(3/14) 전후 성과 변화"""
    if industry in ["뷰티/화장품", "F&B/밀키트", "패션/의류"]:
        if 10 <= day <= 14:
            return 1.3 + (day - 10) * 0.1  # 10일부터 점진 상승, 14일 피크
        elif 15 <= day <= 17:
            return 0.85  # 피크 후 하락
        elif day <= 7:
            return 0.95  # 월초 약세
    elif industry == "반려동물/이커머스":
        if 14 <= day <= 16:
            return 1.1  # 약한 화이트데이 효과
    elif industry == "O2O/배달":
        if day == 14:
            return 1.25  # 화이트데이 당일만 피크
    # 주말 효과
    date = datetime(2026, 3, day)
    if date.weekday() in [5, 6]:  # 토/일
        if industry in ["O2O/배달", "F&B/밀키트"]:
            return 1.15
        elif industry in ["금융/핀테크"]:
            return 0.7
    return 1.0


def add_noise(value, pct=0.15):
    """값에 랜덤 노이즈 추가"""
    return value * random.uniform(1 - pct, 1 + pct)


# === 1. Campaign Daily Performance ===
def generate_campaign_daily():
    rows = []
    for client_name, cfg in CLIENTS.items():
        industry = cfg["industry"]
        campaigns = CAMPAIGN_TEMPLATES[industry]

        for platform in cfg["media_mix"]:
            # 매체별 예산 비중 (현실적 분배)
            media_count = len(cfg["media_mix"])
            if platform == "naver_sa":
                budget_share = 0.30
            elif platform == "meta":
                budget_share = 0.28
            elif platform == "google":
                budget_share = 0.20
            elif platform == "kakao":
                budget_share = 0.12
            elif platform == "naver_gfa":
                budget_share = 0.10
            elif platform == "tiktok":
                budget_share = 0.08
            else:
                budget_share = 1.0 / media_count

            # 실제 사용하는 매체들의 비중 재조정
            daily_budget = (cfg["monthly_budget"] * budget_share) / 31

            for campaign in campaigns:
                campaign_full = f"[{client_name}] {campaign}"

                for day in range(1, 32):
                    date_str = f"2026-03-{day:02d}"

                    seasonal = get_seasonal_multiplier(day, industry)

                    # 캠페인별 성과 변동
                    camp_idx = campaigns.index(campaign)
                    camp_mult = [1.0, 1.15, 0.9, 0.85][camp_idx]  # 캠페인별 성과 차이

                    base_cpc = cfg["base_cpc"][platform]
                    base_ctr = cfg["base_ctr"][platform]
                    base_cvr = cfg["base_cvr"][platform]
                    base_roas = cfg["base_roas"][platform]

                    # 캠페인당 일 예산 (4개 캠페인으로 나눔, 불균등)
                    camp_budget_share = [0.35, 0.30, 0.20, 0.15][camp_idx]
                    spend = daily_budget * camp_budget_share * seasonal * add_noise(1.0, 0.20)
                    spend = max(spend, 10000)  # 최소 1만원

                    cpc = add_noise(base_cpc * camp_mult, 0.20)
                    ctr = add_noise(base_ctr * seasonal, 0.15) / 100

                    clicks = max(int(spend / cpc), 1)
                    impressions = max(int(clicks / ctr), clicks + 1) if ctr > 0 else clicks * 100

                    actual_ctr = (clicks / impressions * 100) if impressions > 0 else 0
                    actual_cpc = spend / clicks if clicks > 0 else 0

                    cvr = add_noise(base_cvr * camp_mult * seasonal, 0.20) / 100
                    conversions = max(int(clicks * cvr), 0)

                    # ROAS 기반 매출 역산 (현실적 ROAS 분포)
                    target_roas = add_noise(base_roas * camp_mult * seasonal, 0.25) / 100
                    revenue = int(spend * target_roas)

                    actual_roas = (revenue / spend * 100) if spend > 0 else 0
                    actual_cvr_pct = (conversions / clicks * 100) if clicks > 0 else 0
                    cpa = (spend / conversions) if conversions > 0 else 0
                    cpm = (spend / impressions * 1000) if impressions > 0 else 0

                    rows.append({
                        "date": date_str,
                        "client_name": client_name,
                        "industry": industry,
                        "platform": PLATFORM_LABELS[platform],
                        "campaign_type": CAMPAIGN_TYPE[platform],
                        "campaign_name": campaign_full,
                        "impressions": impressions,
                        "clicks": clicks,
                        "spend_krw": round(spend),
                        "conversions": conversions,
                        "revenue_krw": revenue,
                        "CTR": round(actual_ctr, 2),
                        "CPC_krw": round(actual_cpc),
                        "CPM_krw": round(cpm),
                        "CVR": round(actual_cvr_pct, 2),
                        "CPA_krw": round(cpa) if conversions > 0 else "",
                        "ROAS": round(actual_roas) if revenue > 0 else 0,
                    })

    return rows


# === 2. Client Master ===
def generate_client_master():
    rows = []
    for i, (client_name, cfg) in enumerate(CLIENTS.items(), 1):
        for platform in cfg["media_mix"]:
            rows.append({
                "client_id": f"CL{i:03d}",
                "client_name": client_name,
                "industry": cfg["industry"],
                "platform": PLATFORM_LABELS[platform],
                "campaign_type": CAMPAIGN_TYPE[platform],
                "contract_type": "마크업" if cfg["kpi_primary"] == "ROAS" else "성과형",
                "monthly_budget_krw": round(cfg["monthly_budget"] * (
                    0.30 if platform == "naver_sa" else
                    0.28 if platform == "meta" else
                    0.20 if platform == "google" else
                    0.12 if platform == "kakao" else
                    0.10 if platform == "naver_gfa" else
                    0.08  # tiktok
                )),
                "commission_rate": cfg["commission_rate"],
                "kpi_primary": cfg["kpi_primary"],
                "kpi_target": cfg["kpi_target"],
                "account_manager": cfg["account_manager"],
                "media_planner": random.choice(["최다은", "한정우", "윤서영"]),
                "contract_start": "2025-10-01" if i <= 3 else "2026-01-01",
                "contract_end": "2026-09-30" if i <= 3 else "2026-12-31",
                "reporting_cycle": "weekly" if cfg["monthly_budget"] >= 150_000_000 else "monthly",
            })
    return rows


# === 3. Creative Performance ===
def generate_creative_performance():
    rows = []
    creative_id = 1

    creative_concepts = {
        "뷰티/화장품": [
            ("image", "feed", "봄 신상 세럼 비포/애프터", "혜택강조"),
            ("video", "reels", "10초 루틴 영상 - 세럼 사용법", "UGC"),
            ("carousel", "feed", "베스트셀러 TOP5 모아보기", "제품나열"),
            ("image", "story", "화이트데이 선물세트 한정판", "시즌프로모"),
            ("video", "feed", "피부과 전문의 추천 영상", "전문가추천"),
            ("image", "feed", "성분 비교 인포그래픽", "정보제공"),
        ],
        "패션/의류": [
            ("image", "feed", "SS 신상 룩북 - 스트릿 캐주얼", "룩북"),
            ("video", "reels", "30초 코디 변신 영상", "UGC"),
            ("carousel", "feed", "커플룩 추천 4가지", "시즌프로모"),
            ("image", "story", "72시간 한정 봄세일 20%", "프로모션"),
            ("video", "feed", "스타일리스트 추천 봄 아이템", "전문가추천"),
        ],
        "F&B/밀키트": [
            ("image", "feed", "봄 신메뉴 비빔밀키트 출시", "신상품"),
            ("video", "reels", "3분 조리 완성 영상", "레시피"),
            ("carousel", "feed", "이번 주 인기 밀키트 TOP3", "제품나열"),
            ("image", "story", "화이트데이 디너세트 15% 할인", "시즌프로모"),
            ("video", "feed", "셰프의 한 마디 - 왜 이 재료인가", "전문가추천"),
        ],
        "반려동물/이커머스": [
            ("image", "feed", "봄맞이 산책 가방 신상", "신상품"),
            ("video", "reels", "강아지 산책 꿀팁 5가지", "정보제공"),
            ("carousel", "feed", "사료 브랜드별 비교", "비교분석"),
            ("image", "story", "첫 구매 30% 할인 쿠폰", "프로모션"),
            ("video", "feed", "수의사 추천 간식 리뷰", "전문가추천"),
            ("image", "feed", "대용량 사료 무료배송 이벤트", "혜택강조"),
        ],
        "금융/핀테크": [
            ("image", "feed", "연 4.5% 예금 상품 안내", "상품소개"),
            ("video", "feed", "1분만에 대출 한도 조회", "기능시연"),
            ("carousel", "feed", "신용카드 혜택 비교 3종", "비교분석"),
            ("image", "story", "가입 즉시 5천원 리워드", "프로모션"),
        ],
        "O2O/배달": [
            ("image", "feed", "신규 가맹점 100곳 오픈", "소식알림"),
            ("video", "reels", "30분 배달 보장 챌린지", "UGC"),
            ("carousel", "feed", "이번 주 맛집 TOP5", "큐레이션"),
            ("image", "story", "첫 주문 5천원 할인", "프로모션"),
            ("video", "feed", "사장님 인터뷰 - 왜 딜리버리킹인가", "브랜드스토리"),
        ],
    }

    platforms_for_creative = ["Meta", "Naver GFA", "Kakao", "TikTok"]  # DA 위주

    for client_name, cfg in CLIENTS.items():
        industry = cfg["industry"]
        concepts = creative_concepts[industry]

        for creative_type, format_type, headline, concept in concepts:
            for platform in cfg["media_mix"]:
                if CAMPAIGN_TYPE[platform] == "SA":
                    continue  # 검색광고는 크리에이티브 분석 대상 아님

                plat_label = PLATFORM_LABELS[platform]

                # 소재 유형별 기본 성과 차이
                type_mult = {"image": 1.0, "video": 1.3, "carousel": 1.15}
                concept_mult = {
                    "UGC": 1.25, "전문가추천": 1.15, "시즌프로모": 1.2,
                    "혜택강조": 1.1, "프로모션": 1.05, "제품나열": 0.95,
                    "신상품": 1.0, "정보제공": 0.9, "레시피": 1.2,
                    "비교분석": 1.0, "룩북": 1.1, "기능시연": 1.05,
                    "소식알림": 0.85, "큐레이션": 1.0, "브랜드스토리": 0.9,
                    "상품소개": 0.95,
                }

                t_mult = type_mult.get(creative_type, 1.0)
                c_mult = concept_mult.get(concept, 1.0)

                base_ctr = cfg["base_ctr"][platform] * t_mult * c_mult
                base_cvr = cfg["base_cvr"][platform] * t_mult

                # 3월 전체 합산
                total_spend = add_noise(
                    cfg["monthly_budget"] * 0.05 * t_mult,  # 소재당 약 5% 예산
                    0.30
                )
                ctr = add_noise(base_ctr, 0.15) / 100
                clicks = max(int(total_spend / add_noise(cfg["base_cpc"][platform], 0.15)), 10)
                impressions = max(int(clicks / ctr), clicks + 1) if ctr > 0 else clicks * 100

                actual_ctr = clicks / impressions * 100 if impressions > 0 else 0

                cvr = add_noise(base_cvr, 0.20) / 100
                conversions = max(int(clicks * cvr), 0)

                # ROAS 기반 매출 역산
                target_roas_cr = add_noise(cfg["base_roas"].get(platform, 350) * t_mult * c_mult, 0.25) / 100
                revenue = int(total_spend * target_roas_cr)
                roas = (revenue / total_spend * 100) if total_spend > 0 else 0

                rows.append({
                    "creative_id": f"CR{creative_id:04d}",
                    "client_name": client_name,
                    "industry": industry,
                    "platform": plat_label,
                    "creative_type": creative_type,
                    "format": format_type,
                    "headline": headline,
                    "creative_concept": concept,
                    "impressions": impressions,
                    "clicks": clicks,
                    "spend_krw": round(total_spend),
                    "conversions": conversions,
                    "revenue_krw": revenue,
                    "CTR": round(actual_ctr, 2),
                    "CVR": round(conversions / clicks * 100, 2) if clicks > 0 else 0,
                    "ROAS": round(roas),
                })
                creative_id += 1

    return rows


# === 4. Competitor Benchmark ===
def generate_competitor_benchmark():
    competitors = [
        {
            "agency_name": "매드업",
            "type": "퍼포먼스+SaaS",
            "specialty": "애드테크 SaaS (LEVER Xpert)",
            "employee_count": 350,
            "annual_billings_billion_krw": 3500,
            "avg_roas_beauty": 380,
            "avg_roas_fashion": 340,
            "avg_roas_fnb": 520,
            "avg_roas_ecommerce": 420,
            "avg_ctr_meta": 1.8,
            "avg_ctr_naver_sa": 5.2,
            "strength": "자체 AI 솔루션, 50명 개발조직",
            "weakness": "대형 광고주 부족",
        },
        {
            "agency_name": "에코마케팅",
            "type": "퍼포먼스",
            "specialty": "D2C 브랜드 육성",
            "employee_count": 280,
            "annual_billings_billion_krw": 2800,
            "avg_roas_beauty": 420,
            "avg_roas_fashion": 310,
            "avg_roas_fnb": 480,
            "avg_roas_ecommerce": 460,
            "avg_ctr_meta": 2.0,
            "avg_ctr_naver_sa": 4.8,
            "strength": "자체 브랜드 보유 (클럭, 몽제), Revenue Share 모델",
            "weakness": "자체 브랜드 집중으로 대행 비중 감소",
        },
        {
            "agency_name": "인크로스",
            "type": "미디어렙",
            "specialty": "SK 계열 미디어 네트워크",
            "employee_count": 200,
            "annual_billings_billion_krw": 4200,
            "avg_roas_beauty": 350,
            "avg_roas_fashion": 300,
            "avg_roas_fnb": 450,
            "avg_roas_ecommerce": 380,
            "avg_ctr_meta": 1.5,
            "avg_ctr_naver_sa": 4.5,
            "strength": "SK 미디어 네트워크 독점, T커머스 연동",
            "weakness": "SK 의존도 높음, 독립 퍼포먼스 약함",
        },
        {
            "agency_name": "나스미디어",
            "type": "미디어렙",
            "specialty": "KT 계열, 종합 미디어 플래닝",
            "employee_count": 350,
            "annual_billings_billion_krw": 5500,
            "avg_roas_beauty": 330,
            "avg_roas_fashion": 290,
            "avg_roas_fnb": 420,
            "avg_roas_ecommerce": 370,
            "avg_ctr_meta": 1.4,
            "avg_ctr_naver_sa": 4.2,
            "strength": "대형 광고주 포트폴리오, KT 시너지",
            "weakness": "퍼포먼스 특화 부족, 브랜딩 중심",
        },
        {
            "agency_name": "플레이디",
            "type": "디지털 에이전시",
            "specialty": "롯데 계열, 통합 디지털 마케팅",
            "employee_count": 400,
            "annual_billings_billion_krw": 4000,
            "avg_roas_beauty": 360,
            "avg_roas_fashion": 320,
            "avg_roas_fnb": 460,
            "avg_roas_ecommerce": 400,
            "avg_ctr_meta": 1.6,
            "avg_ctr_naver_sa": 4.6,
            "strength": "롯데 계열사 안정적 물량, 통합 마케팅",
            "weakness": "롯데 의존, 독립 고객 확장 제한",
        },
        {
            "agency_name": "이엠넷",
            "type": "검색광고 전문",
            "specialty": "네이버/구글 검색광고 최적화",
            "employee_count": 150,
            "annual_billings_billion_krw": 1800,
            "avg_roas_beauty": 400,
            "avg_roas_fashion": 350,
            "avg_roas_fnb": 550,
            "avg_roas_ecommerce": 450,
            "avg_ctr_meta": 1.3,
            "avg_ctr_naver_sa": 6.0,
            "strength": "검색광고 전문성, 높은 SA ROAS",
            "weakness": "DA/영상 약함, 규모 제한",
        },
        {
            "agency_name": "차이커뮤니케이션",
            "type": "콘텐츠+퍼포먼스",
            "specialty": "크리에이티브 중심 퍼포먼스",
            "employee_count": 220,
            "annual_billings_billion_krw": 2200,
            "avg_roas_beauty": 370,
            "avg_roas_fashion": 380,
            "avg_roas_fnb": 440,
            "avg_roas_ecommerce": 390,
            "avg_ctr_meta": 2.1,
            "avg_ctr_naver_sa": 4.3,
            "strength": "크리에이티브 퀄리티, 콘텐츠 마케팅 역량",
            "weakness": "테크 투자 부족, SaaS 없음",
        },
        {
            "agency_name": "와이즈버즈",
            "type": "퍼포먼스",
            "specialty": "SNS 광고 전문 (Meta, TikTok)",
            "employee_count": 180,
            "annual_billings_billion_krw": 2000,
            "avg_roas_beauty": 390,
            "avg_roas_fashion": 360,
            "avg_roas_fnb": 470,
            "avg_roas_ecommerce": 410,
            "avg_ctr_meta": 2.2,
            "avg_ctr_naver_sa": 3.8,
            "strength": "Meta/TikTok 공식 파트너, SNS DA 강점",
            "weakness": "검색광고 약함, 네이버 SA 경쟁력 부족",
        },
    ]
    return competitors


# === 파일 생성 ===
OUTPUT_DIR = "/Users/rhim/Projects/do-better-workspace/50-resources/sample-data/madup"

# 1. Campaign Daily
campaign_data = generate_campaign_daily()
with open(f"{OUTPUT_DIR}/madup_campaign_daily_2603.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=campaign_data[0].keys())
    writer.writeheader()
    writer.writerows(campaign_data)
print(f"Campaign daily: {len(campaign_data)}건")

# 2. Client Master
client_data = generate_client_master()
with open(f"{OUTPUT_DIR}/madup_client_master.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=client_data[0].keys())
    writer.writeheader()
    writer.writerows(client_data)
print(f"Client master: {len(client_data)}건")

# 3. Creative Performance
creative_data = generate_creative_performance()
with open(f"{OUTPUT_DIR}/madup_creative_performance_2603.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=creative_data[0].keys())
    writer.writeheader()
    writer.writerows(creative_data)
print(f"Creative performance: {len(creative_data)}건")

# 4. Competitor Benchmark
competitor_data = generate_competitor_benchmark()
# competitor는 필드가 다를 수 있으므로 모든 키 수집
all_keys = []
for row in competitor_data:
    for k in row.keys():
        if k not in all_keys:
            all_keys.append(k)

with open(f"{OUTPUT_DIR}/madup_competitor_benchmark.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=all_keys)
    writer.writeheader()
    writer.writerows(competitor_data)
print(f"Competitor benchmark: {len(competitor_data)}건")

print("\n=== 완료 ===")
