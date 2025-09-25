from fastapi import FastAPI, Query
from pydantic import BaseModel
import os
import asyncio

from .providers.localdemo import Local
from .providers.justwatch import JW
from .providers.serialized import SZ

app = FastAPI(title="AU TV Recommender API", version="0.3.0")

def pick_provider():
    prov = os.getenv("PROVIDER", "local").lower()
    if prov == "justwatch":
        return JW()
    if prov == "serialized":
        return SZ()
    return Local()

class RecRequest(BaseModel):
    user_id: str | None = None
    limit: int = 10
    max_age: int | None = None
    include_tags: list[str] | None = None
    exclude_tags: list[str] | None = None

def keep(req: RecRequest, item: dict) -> bool:
    if req.include_tags:
        if not set(t.lower() for t in req.include_tags).issubset({t.lower() for t in item.get("tags", [])}):
            return False
    if req.exclude_tags:
        if {t.lower() for t in item.get("tags", [])} & {t.lower() for t in req.exclude_tags}:
            return False
    return True

@app.get("/readyz")
async def readyz():
    return {"status": "ok", "version": app.version}

@app.get("/shows")
async def shows(q: str | None = Query(default=None), limit: int = 20):
    prov = pick_provider()
    items = await prov.search(q=q, limit=limit)
    return {"source": getattr(prov, "name", "?"), "items": items}

@app.post("/recommendations")
async def recommendations(req: RecRequest):
    prov = pick_provider()
    items = await prov.search(q=None, limit=200)
    items = [i for i in items if keep(req, i)]
    items = items[: req.limit]
    return {"user_id": req.user_id, "source": getattr(prov, "name", "?"), "items": items}
