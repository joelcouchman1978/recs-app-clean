import os
from typing import Iterable, Optional, Dict, Any
import httpx

# Serialized adapter (placeholder GraphQL/REST). Fill SERIALIZED_API_KEY to activate.
# Environment:
#   SERIALIZED_BASE=https://api.serialized.app
#   SERIALIZED_API_KEY=...    (required)

class SZ:
    name = "serialized"
    def __init__(self):
        self.base = os.getenv("SERIALIZED_BASE", "https://api.serialized.app")
        self.key  = os.getenv("SERIALIZED_API_KEY","")

    def _hdrs(self):
        if not self.key:
            raise RuntimeError("SERIALIZED_API_KEY not set")
        return {"Authorization": f"Bearer {self.key}"}

    def _norm(self, s: Dict[str,Any]) -> Dict[str,Any]:
        return {
            "id": str(s.get("id") or s.get("_id") or s.get("slug") or ""),
            "title": s.get("title") or s.get("name") or "",
            "year_start": s.get("year") or s.get("first_air_year") or None,
            "tags": s.get("tags") or [],
            "source": "serialized",
        }

    async def popular(self, limit: int=20) -> Iterable[Dict[str,Any]]:
        # Placeholder endpoint — adjust to the real one your account supports.
        url = f"{self.base}/v1/popular"
        async with httpx.AsyncClient(timeout=20, headers=self._hdrs()) as s:
            r = await s.get(url, params={"limit": limit})
            r.raise_for_status()
            data = r.json()
        items = data.get("results") or data
        return [self._norm(x) for x in items[:limit]]

    async def search(self, q: Optional[str]=None, limit: int=20) -> Iterable[Dict[str,Any]]:
        if not q:
            return await self.popular(limit=limit)
        url = f"{self.base}/v1/search"
        async with httpx.AsyncClient(timeout=20, headers=self._hdrs()) as s:
            r = await s.get(url, params={"q": q, "limit": limit})
            r.raise_for_status()
            data = r.json()
        items = data.get("results") or data
        return [self._norm(x) for x in items[:limit]]
