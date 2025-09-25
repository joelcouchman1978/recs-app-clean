from typing import Iterable, Optional, Dict, Any

CATALOG = [
  {"id":"bb","title":"Breaking Bad","year_start":2008,"tags":["crime","drama"]},
  {"id":"got","title":"Game of Thrones","year_start":2011,"tags":["fantasy","drama"]},
  {"id":"ofmd","title":"Our Flag Means Death","year_start":2022,"tags":["comedy","romance"]},
  {"id":"bn99","title":"Brooklyn Nine-Nine","year_start":2013,"tags":["comedy","police"]},
  {"id":"bletch","title":"The Bletchley Circle","year_start":2012,"tags":["mystery","drama"]},
  {"id":"bluey","title":"Bluey","year_start":2018,"tags":["kids","family"]},
]

class Local:
    name = "local"
    async def popular(self, limit: int=20) -> Iterable[Dict[str,Any]]:
        return CATALOG[:limit]
    async def search(self, q: Optional[str]=None, limit: int=20) -> Iterable[Dict[str,Any]]:
        if not q: return await self.popular(limit)
        ql=q.lower()
        return [s for s in CATALOG if ql in s["title"].lower()][:limit]
