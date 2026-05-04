"""KOSIS (국가통계포털) API — 인구·사회 통계 보강."""

import os
import httpx

KOSIS_KEY = os.environ.get("KOSIS_API_KEY", "")
BASE_URL = "https://kosis.kr/openapi"


async def fetch_population_kosis(adong_cd: str = "1144062500", year: str = "2024") -> dict:
    """KOSIS 인구통계 — 행안부 미작동 시 보강용.

    실제 사용 시 통계표 ID(orgId·tblId)를 미리 확인해야 함.
    """
    url = f"{BASE_URL}/Param/statisticsParameterData.do"
    params = {
        "method": "getList",
        "apiKey": KOSIS_KEY,
        "format": "json",
        "jsonVD": "Y",
        "newEstPrdCnt": "1",
        "prdSe": "Y",
        "orgId": "101",       # 통계청
        "tblId": "DT_1IN1502",  # 인구주택총조사 — 예시
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            data = r.json() if "json" in r.headers.get("content-type", "") else {"raw_text": r.text}
            return {"ok": True, "raw": data, "source": "KOSIS_인구"}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "KOSIS_인구"}


async def search_statistic_tables(category_id: str = "A21") -> dict:
    """KOSIS 통계표 검색 — 통계표 ID 찾기 보조."""
    url = f"{BASE_URL}/statisticsList.do"
    params = {
        "method": "getList",
        "apiKey": KOSIS_KEY,
        "format": "json",
        "jsonVD": "Y",
        "vwCd": "MT_ZTITLE",
        "parentListId": category_id,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(url, params=params)
            data = r.json() if "json" in r.headers.get("content-type", "") else {"raw_text": r.text}
            return {"ok": True, "raw": data, "source": "KOSIS_검색"}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "KOSIS_검색"}
