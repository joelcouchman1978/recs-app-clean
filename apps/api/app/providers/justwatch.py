import os, asyncio, json
from typing import Iterable, Optional, Dict, Any
import httpx

# Minimal JustWatch adapter (AU by default). Public endpoints are unstable; this may need tweaks later.
# Environment:
#   JUSTWATCH_BASE=https://apis.justwatch.com
#   JUSTWATCH_LOCALE=en_AU
#   JUSTWATCH_REGION=AU

class JW:
    name = "justwatch"
    def __init__(self):
        self.base = os.getenv("JUSTWATCH_BASE", "https://apis.justwatch.com")
        self.locale = os.getenv("JUSTWATCH_LOCALE", "en_AU")

    def _norm(self, item: Dict[str, Any]) -> Dict[str, Any]:
        title = item.get("title") or item.get("original_title") or ""
        year = (item.get("original_release_year")
                or item.get("cinema_release_year")
                or item.get("localized_release_date", {}).get("year")
                or None)
        return {
            "id": str(item.get("id")),
            "title": title,
            "year_start": year,
            "tags": [g.get("translation") or g.get("technical_name","") for g in item.get("genres",[]) if g] or [],
            "source": "justwatch",
        }

    async def popular(self, limit: int=20) -> Iterable[Dict[str,Any]]:
        url = f"{self.base}/content/titles/{self.locale}/popular"
        async with httpx.AsyncClient(timeout=20) as s:
            # Basic body; adjust filters later as needed
            r = await s.post(url, json={"page_size": max(1,min(limit,50))})
            r.raise_for_status()
            data = r.json()
        items = data.get("items") or data
        return [self._norm(x) for x in items[:limit]]

    async def search(self, q: Optional[str]=None, limit: int=20) -> Iterable[Dict[str,Any]]:
        if not q:
            return await self.popular(limit=limit)
        url = f"{self.base}/content/titles/{self.locale}/popular"
        async with httpx.AsyncClient(timeout=20) as s:
            r = await s.post(url, json={"page_size": max(1,min(limit,50)), "query": q})
            r.raise_for_status()
            data = r.json()
        items = data.get("items") or data
        return [self._norm(x) for x in items[:limit]]
