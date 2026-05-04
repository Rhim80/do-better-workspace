"""공공데이터포털 API — 행안부 인구 + 소진공 상가."""

import os
import asyncio
import httpx
from typing import Optional

DATAGOKR_KEY = os.environ.get("DATAGOKR_API_KEY", "")


async def fetch_population(adong_cd: str, ymd: str = "202412") -> dict:
    """행정안전부 행정동별(통반단위) 주민등록 인구 및 세대현황.

    Args:
        adong_cd: 행정동 10자리 코드 또는 stdgCd
        ymd: 기준 연월 (YYYYMM)
    """
    url = "http://apis.data.go.kr/1741000/admmPpltnHhStus/selectAdmmPpltnHhStus"
    params = {
        "serviceKey": DATAGOKR_KEY,
        "type": "json",
        "pageNo": "1",
        "numOfRows": "100",
        "stdgCd": adong_cd[:7] if len(adong_cd) >= 7 else adong_cd,  # 행안부는 7자리 stdgCd 가능
        "stdgYmd": ymd,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(url, params=params)
            data = r.json()
            return {"ok": True, "raw": data, "source": "행안부_통반단위_인구"}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "행안부_통반단위_인구"}


async def fetch_stores(adong_cd: str, num_rows: int = 1000) -> dict:
    """소상공인시장진흥공단 상가(상권)정보 — 행정동 단위.

    Args:
        adong_cd: 행정동 10자리 코드 (예: 1144062500 = 서교동)
        num_rows: 최대 1,000
    """
    url = "https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong"
    params = {
        "serviceKey": DATAGOKR_KEY,
        "divId": "adongCd",
        "key": adong_cd,
        "type": "json",
        "pageNo": "1",
        "numOfRows": str(num_rows),
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            data = r.json()
            return {"ok": True, "raw": data, "source": "소진공_상가정보"}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "소진공_상가정보"}


async def fetch_realestate_offi(signgu_cd: str, deal_ymd: str = "202412") -> dict:
    """국토부 상업업무용 부동산 매매 실거래가.

    NOTE: 정확한 endpoint URL 미확인. 사용자 마이페이지에서 참고문서 받은 후 수정 필요.
    현재는 시도 endpoint들로 fallback.
    """
    candidates = [
        # 가능성 높은 endpoint 순서대로 시도
        "https://apis.data.go.kr/1613000/RTMSDataSvcStoreTrade/getRTMSDataSvcStoreTrade",
        "https://apis.data.go.kr/1613000/RTMSDataSvcCmrcTrade/getRTMSDataSvcCmrcTrade",
        "https://apis.data.go.kr/1613000/RTMSDataSvcSBTrade/getRTMSDataSvcSBTrade",
    ]
    params_base = {
        "serviceKey": DATAGOKR_KEY,
        "LAWD_CD": signgu_cd,
        "DEAL_YMD": deal_ymd,
        "pageNo": "1",
        "numOfRows": "100",
        "_type": "json",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        for url in candidates:
            try:
                r = await client.get(url, params=params_base)
                if r.status_code == 200 and "Forbidden" not in r.text and "errors" not in r.text.lower():
                    return {"ok": True, "raw": r.json() if "json" in r.headers.get("content-type", "") else r.text, "source": "국토부_상업업무용_매매", "endpoint": url}
            except Exception:
                continue
        return {"ok": False, "error": "endpoint URL 미확인. 사용자 참고문서 필요.", "source": "국토부_상업업무용_매매"}


async def fetch_foreign_visit(year: str = "2024", sido_cd: str = "A") -> dict:
    """한국문화관광연구원 외래관광객 관광실태조사.

    NOTE: 정확한 endpoint URL 미확인. 사용자 참고문서 필요.
    """
    candidates = [
        "https://apis.data.go.kr/B551011/TarRlteTarService/areaBasedList",
        "https://apis.data.go.kr/1051000/ForeignVisitorService/getForeignVisitorList",
    ]
    params_base = {
        "serviceKey": DATAGOKR_KEY,
        "MobileOS": "ETC",
        "MobileApp": "zone-fetch",
        "_type": "json",
        "numOfRows": "100",
        "pageNo": "1",
        "YY": year,
        "SIDO_CD": sido_cd,
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        for url in candidates:
            try:
                r = await client.get(url, params=params_base)
                if r.status_code == 200 and "Forbidden" not in r.text:
                    return {"ok": True, "raw": r.text, "source": "관광공사_외래관광객", "endpoint": url}
            except Exception:
                continue
        return {"ok": False, "error": "endpoint URL 미확인. 사용자 참고문서 필요.", "source": "관광공사_외래관광객"}
