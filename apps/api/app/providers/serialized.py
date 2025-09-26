from typing import List, Dict, Any

class SZ:
    name = "serialized"

    def __init__(self) -> None:
        self._catalog: List[Dict[str, Any]] = [
            {"id": "sz-1", "title": "Serialized Thriller S1", "tags": ["thriller", "series"]},
            {"id": "sz-2", "title": "Serialized Comedy S2", "tags": ["comedy", "series"]},
            {"id": "sz-3", "title": "Serialized Drama S3", "tags": ["drama", "series"]},
        ]

    async def search(self, q: str | None, limit: int = 20):
        items = self._catalog
        if q:
            ql = q.lower()
            items = [i for i in items if ql in i["title"].lower()]
        return items[: max(0, limit)]
