"""Google Trends — pytrends 라이브러리. 키 불필요.

사용 전 설치: pip install pytrends
"""

from typing import Optional


async def fetch_search_interest(keyword: str, geo: str = "KR", timeframe: str = "today 12-m") -> dict:
    """Google Trends 검색 관심도 시계열.

    Args:
        keyword: "한남동 카페" 같은 검색어
        geo: 국가 코드 (KR=한국)
        timeframe: 'today 12-m' (12개월), 'today 5-y' (5년) 등
    """
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return {"ok": False, "error": "pytrends 미설치. pip install pytrends", "source": "GoogleTrends"}

    try:
        # pytrends는 동기 API. asyncio executor에서 실행 권장.
        import asyncio
        loop = asyncio.get_event_loop()

        def _fetch():
            pytrend = TrendReq(hl="ko-KR", tz=540)
            pytrend.build_payload([keyword], geo=geo, timeframe=timeframe)
            df = pytrend.interest_over_time()
            if df.empty:
                return {"data": [], "trend": "데이터 없음"}
            monthly = [
                {"month": str(idx.date())[:7], "value": int(row[keyword])}
                for idx, row in df.iterrows()
            ]
            first, last = monthly[0]["value"], monthly[-1]["value"]
            trend_pct = round((last - first) / max(first, 1) * 100, 1)
            return {
                "keyword": keyword,
                "monthly": monthly,
                "trend": f"{trend_pct:+.0f}% (12개월)",
            }

        result = await loop.run_in_executor(None, _fetch)
        return {"ok": True, "raw": result, "source": "GoogleTrends"}
    except Exception as e:
        return {"ok": False, "error": str(e), "source": "GoogleTrends"}
