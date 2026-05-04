"""zone-fetch orchestrator — 12개 소스 병렬 호출 + zone-cache JSON 생성.

사용:
    python -m modules.orchestrator 한남동

Output:
    50-resources/data/zone-cache/{zone_name}.json
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# .env.local 로드
def load_env(env_path: str = ".env.local"):
    if not os.path.exists(env_path):
        env_path = "../../../.env.local"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()

from . import zone_codes, public_api, seoul_api, rone_api, kosis_api, pytrends_module


async def fetch_all_sources(zone_name: str) -> dict:
    """zone에 대한 모든 소스 병렬 호출."""
    z = zone_codes.resolve(zone_name)
    if not z:
        raise ValueError(f"Unknown zone: {zone_name}. Known: {zone_codes.list_zones()}")

    keyword = z.get("search_kw", f"{zone_name} 카페")
    trdar_kw = z.get("trdar_keyword", zone_name[:2])

    # 12개 소스 병렬 호출
    tasks = {
        "행안부_인구": public_api.fetch_population(z["adong_cd"], "202412"),
        "소진공_상가": public_api.fetch_stores(z["adong_cd"]),
        "국토부_매매": public_api.fetch_realestate_offi(z["signgu_cd"], "202412"),
        "관광공사_외국인": public_api.fetch_foreign_visit("2024", "A"),
        "KT_생활인구": seoul_api.fetch_living_pop(z["adong_cd"], "20241231"),
        "추정매출": seoul_api.fetch_sales_estimate(trdar_kw, "20244"),
        "상권변화": seoul_api.fetch_zone_change(trdar_kw, "20244"),
        "R-One_임대료": rone_api.fetch_rone_rent(z["signgu_cd"], "2024", "4"),
        "KOSIS_인구": kosis_api.fetch_population_kosis(z["adong_cd"], "2024"),
        "GoogleTrends": pytrends_module.fetch_search_interest(keyword),
    }

    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    return dict(zip(tasks.keys(), results))


def build_zone_cache(zone_name: str, raw_results: dict) -> dict:
    """raw 결과를 zone-cache 표준 스키마로 변환."""
    z = zone_codes.resolve(zone_name)
    sources = {}
    for src, result in raw_results.items():
        if isinstance(result, dict):
            sources[src] = {
                "ok": result.get("ok", False),
                "error": result.get("error"),
                "fetched_at": datetime.now().isoformat(),
            }
        else:
            sources[src] = {"ok": False, "error": str(result)}

    cache = {
        "zone_id": z["adong_cd"],
        "zone_name": zone_name,
        "alias": z["alias"],
        "geo": {"lat": z["lat"], "lng": z["lng"], "radius_m": 500},
        "fetched_at": datetime.now().isoformat(),
        "is_mock": False,
        "sources": sources,
        "raw_data": {k: (v.get("raw") if isinstance(v, dict) else None) for k, v in raw_results.items()},
        "_note": "실시간 수집. 정규화는 zone-diagnosis/entry-verdict가 raw_data에서 수행.",
    }
    return cache


async def main(zone_name: str):
    print(f"[zone-fetch] {zone_name} 호출 시작...")
    raw = await fetch_all_sources(zone_name)

    print(f"[zone-fetch] 결과 요약:")
    for src, result in raw.items():
        ok = result.get("ok") if isinstance(result, dict) else False
        mark = "✅" if ok else "❌"
        err = result.get("error", "") if isinstance(result, dict) else str(result)[:60]
        print(f"  {mark} {src:20s} {err if not ok else 'OK'}")

    cache = build_zone_cache(zone_name, raw)

    # 저장 — PROJECT_ROOT 기준 (zone-fetch 모듈 위치에서 4단계 위)
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    out_dir = project_root / "50-resources" / "data" / "zone-cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{zone_name}.live.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    print(f"[zone-fetch] 저장: {out_path}")
    return cache


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python -m modules.orchestrator <zone_name>")
        print(f"Available: {zone_codes.list_zones()}")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
