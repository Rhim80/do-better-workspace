"""한국부동산원 R-One API — 상가 임대 시세 통계."""

import os
import httpx

RONE_KEY = os.environ.get("RONE_API_KEY", "")
BASE_URL = "https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do"

# 상가 임대료 통계 통계표 ID (R-One 상가건물 임대 시세 분기별 통계)
# 정확한 STATBL_ID는 R-One 통계표 검색에서 확인. 여기는 가능성 높은 후보.
STATBL_CANDIDATES = {
    "상가임대료": "A_2024_00150",  # 분기별 상가건물 임대료지수
    "상가공실률": "A_2024_00153",  # 상가건물 공실률
    "상가투자수익률": "A_2024_00155",  # 상가건물 투자수익률
}


async def fetch_rone_rent(signgu_cd: str = "11440", year: str = "2024", quarter: str = "4") -> dict:
    """R-One 상가 임대료 통계.

    Args:
        signgu_cd: 시군구 코드 (5자리)
        year: 연도
        quarter: 분기 (1-4)
    """
    statbl_id = STATBL_CANDIDATES["상가임대료"]
    params = {
        "KEY": RONE_KEY,
        "Type": "json",
        "pIndex": "1",
        "pSize": "1000",
        "STATBL_ID": statbl_id,
        "DTACYCLE_CD": "QY",  # 분기별
        "WRTTIME_IDTFR_ID": f"{year}Q{quarter}",
    }
    async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
        try:
            r = await client.get(BASE_URL, params=params)
            data = r.json() if "json" in r.headers.get("content-type", "") else {"raw_text": r.text}
            return {"ok": True, "raw": data, "source": "R-One_상가임대료", "statbl_id": statbl_id}
        except Exception as e:
            return {"ok": False, "error": str(e), "source": "R-One_상가임대료"}
