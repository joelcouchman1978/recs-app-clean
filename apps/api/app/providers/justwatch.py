from typing import List, Dict, Any

class JW:
    name = "justwatch"

    def __init__(self) -> None:
        self._catalog: List[Dict[str, Any]] = [
            {"id": "jw-1", "title": "Aussie Crime Series", "tags": ["crime", "au", "tv"]},
            {"id": "jw-2", "title": "Family Movie Night", "tags": ["family", "film"]},
            {"id": "jw-3", "title": "Documentary Shorts", "tags": ["doco", "shorts"]},
        ]

    async def search(self, q: str | None, limit: int = 20):
        items = self._catalog
        if q:
            ql = q.lower()
            items = [i for i in items if ql in i["title"].lower()]
        return items[: max(0, limit)]
