from typing import List, Dict, Any

class Local:
    name = "local"

    def __init__(self) -> None:
        self._catalog: List[Dict[str, Any]] = [
            {"id": "loc-1", "title": "Blue Mountains Documentary", "tags": ["nature", "au", "free"]},
            {"id": "loc-2", "title": "Sydney Indie Film Night", "tags": ["indie", "au"]},
            {"id": "loc-3", "title": "Classic Rugby League Finals", "tags": ["sport", "nrl", "au"]},
            {"id": "loc-4", "title": "World Cinema Picks", "tags": ["world", "arthouse"]},
            {"id": "loc-5", "title": "Science Weekly", "tags": ["science", "education"]},
        ]

    async def search(self, q: str | None, limit: int = 20):
        items = self._catalog
        if q:
            ql = q.lower()
            items = [i for i in items if ql in i["title"].lower()]
        return items[: max(0, limit)]
