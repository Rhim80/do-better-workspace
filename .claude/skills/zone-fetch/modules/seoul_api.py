"""서울 열린데이터 광장 API — KT 생활인구 + 우리마을가게 추정매출 + 상권변화."""

import os
import httpx

SEOUL_KEY = os.environ.get("SEOUL_OPENDATA_API_KEY", "")
BASE_URL = "http://openapi.seoul.go.kr:8088"


async def fetch_living_pop(adong_cd: str, ymd: str = "20241231") -> dict:
    """KT 생활인구 — 다양한 서비스명 fallback 시도.

    서울 열린데이터의 생활인구 서비스 후보:
    - SPOP_LOCAL_RESD_DONG (행정동 단위, 코드 형식 문제 가능)
    - SeoulRtdAvrgAge (실시간 도시데이터 평균 연령)
    - VwsmAdstrdFlpopW (행정동 길단위 인구 분기별)
    """
    candidates = [
        ("VwsmAdstrdFlpopW", f"{BASE_URL}/{SEOUL_KEY}/json/VwsmAdstrdFlpopW/1/100/20244"),
        ("SPOP_LOCAL_RESD_DONG", f"{BASE_URL}/{SEOUL_KEY}/json/SPOP_LOCAL_RESD_DONG/1/100/{ymd}/{adong_cd}"),
    ]
    async with httpx.AsyncClient(timeout=10.0) as client:
        for service_name, url in candidates:
            try:
                r = await client.get(url)
                data = r.json()
                code = data.get(service_name, {}).get("RESULT", {}).get("CODE", "")
                if code == "INFO-000":
                    return {"ok": True, "raw": data, "source": "KT_생활인구", "service": service_name}
            except Exception:
                continue
        return {"ok": False, "error": "서비스명 또는 행정동 코드 매핑 필요", "source": "KT_생활인구"}


async def fetch_sales_estimate(zone_keyword: str = "한남", qtr: str = "20244", page_size: int = 1000) -> dict:
    """우리마을가게 추정매출 (분기) — 서울시 상권(TRDAR) 단위.

    서비스: VwsmTrdarSelngQq. 21,664건 중 zone_keyword 매칭하여 필터링.

    Args:
        zone_keyword: 상권명 키워드 (예: "한남", "홍대", "성수", "압구정")
        qtr: YYYYQ (20244 = 2024년 4분기)
        page_size: 한 번에 가져올 row 수 (최대 1,000)
    """
    url = f"{BASE_URL}/{SEOUL_KEY}/json/VwsmTrdarSelngQq/1/{page_size}/{qtr}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url)
            data = r.json()
            ok = data.get("VwsmTrdarSelngQq", {}).get("RESULT", {}).get("CODE", "") == "INFO-000"
            if ok:
                rows = data.get("VwsmTrdarSelngQq", {}).get("row", [])
                # zone_keyword가 상권명에 포함된 row만 필터링
                filtered = [r for r in rows if zone_keyword in r.get("TRDAR_CD_NM", "")]
                return {"ok": True, "raw": data, "filtered": filtered, "filter_keyword": zone_keyword, "source": "우리마을가게_추정매출"}
            return {"ok": False, "raw": data, "source": "우리마을가게_추정매출"}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "우리마을가게_추정매출"}


async def fetch_zone_change(zone_keyword: str = "한남", qtr: str = "20244") -> dict:
    """상권변화지표 (분기) — VwsmTrdarChangeIndicatorQq 또는 fallback."""
    candidates = [
        ("VwsmTrdarChangeIndicatorQq", f"{BASE_URL}/{SEOUL_KEY}/json/VwsmTrdarChangeIndicatorQq/1/1000/{qtr}"),
        ("VwsmTrdarStorQq", f"{BASE_URL}/{SEOUL_KEY}/json/VwsmTrdarStorQq/1/1000/{qtr}"),
    ]
    async with httpx.AsyncClient(timeout=10.0) as client:
        for service_name, url in candidates:
            try:
                r = await client.get(url)
                data = r.json()
                code = data.get(service_name, {}).get("RESULT", {}).get("CODE", "")
                if code == "INFO-000":
                    rows = data.get(service_name, {}).get("row", [])
                    filtered = [r for r in rows if zone_keyword in r.get("TRDAR_CD_NM", "")]
                    return {"ok": True, "raw": data, "filtered": filtered, "source": "상권변화지표", "service": service_name}
            except Exception:
                continue
        return {"ok": False, "error": "서비스명 매핑 필요", "source": "상권변화지표"}
