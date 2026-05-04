"""행정동 ↔ 시군구 ↔ zone 이름 매핑 (시연 4개 + 확장 가능)."""

# 시연 4개 zone (zone-cache mock과 일치)
ZONE_MAP = {
    "홍대입구": {
        "alias": "마포구 서교동",
        "stdg_cd": "1144000000",
        "signgu_cd": "11440",
        "adong_cd": "1144062500",
        "lat": 37.5563,
        "lng": 126.9236,
        "trdar_keyword": "홍대",  # 서울 상권명 매칭 키워드
        "search_kw": "홍대 카페",
    },
    "한남동": {
        "alias": "용산구 한남동",
        "stdg_cd": "1117000000",
        "signgu_cd": "11170",
        "adong_cd": "1117073000",
        "lat": 37.5350,
        "lng": 127.0010,
        "trdar_keyword": "한남",
        "search_kw": "한남동 카페",
    },
    "성수동": {
        "alias": "성동구 성수동1가",
        "stdg_cd": "1120000000",
        "signgu_cd": "11200",
        "adong_cd": "1120053000",
        "lat": 37.5447,
        "lng": 127.0557,
        "trdar_keyword": "성수",
        "search_kw": "성수동 카페",
    },
    "압구정동": {
        "alias": "강남구 압구정동",
        "stdg_cd": "1168000000",
        "signgu_cd": "11680",
        "adong_cd": "1168058000",
        "lat": 37.5274,
        "lng": 127.0288,
        "trdar_keyword": "압구정",
        "search_kw": "압구정 카페",
    },
}


def resolve(zone_name: str) -> dict:
    """zone 이름 → 코드 매핑. 모르면 None."""
    return ZONE_MAP.get(zone_name)


def list_zones() -> list[str]:
    return list(ZONE_MAP.keys())
