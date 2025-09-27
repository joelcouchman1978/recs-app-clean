from fastapi import FastAPI, Query, Response, Response, Response
from pydantic import BaseModel
import os
import asyncio

from .providers.localdemo import Local
from .providers.justwatch import JW
from .providers.serialized import SZ

app = FastAPI(title="AU TV Recommender API", version="0.3.0")



from prometheus_client import CollectorRegistry, Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
_registry = CollectorRegistry()
_reqs_latency = Histogram("recs_request_latency_ms", "Request latency", buckets=[1,5,10,25,50,100,250,500,1000], registry=_registry)
_cache_hits = Counter("recs_cache_hits_total", "Cache hits", registry=_registry)
_cache_misses = Counter("recs_cache_misses_total", "Cache misses", registry=_registry)
_stale_ratio = Histogram("recs_stale_ratio_bucket", "Stale ratio", buckets=[0,0.25,0.5,0.75,1.0], registry=_registry)
_build_info = Gauge("recs_build_info", "Build info", ["version"], registry=_registry)
_build_info.labels(version=app.version).set(1)

@app.get("/metrics")
async def metrics():
    try:
        _reqs_latency.observe(0.0)
    except Exception:
        pass
    try:
        _cache_hits.inc(0); _cache_misses.inc(0)
    except Exception:
        pass
    try:
        _stale_ratio.observe(0.0)
    except Exception:
        pass
    data = generate_latest(_registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
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
async def recommendations_post(req: RecRequest):
    prov = pick_provider()
    items = await prov.search(q=None, limit=200)
    items = [i for i in items if keep(req, i)]
    return {"user_id": req.user_id, "source": getattr(prov, "name", "?"), "items": items[: req.limit]}
from fastapi import FastAPI, Query, Response, Response, Response
from pydantic import BaseModel
import os
import asyncio

from .providers.localdemo import Local
from .providers.justwatch import JW
from .providers.serialized import SZ





@app.get("/recommendations")
async def recommendations_get(for_: str | None = Query(default=None, alias="for"), seed: int | None = None, intent: str | None = None, explain: bool | None = None, limit: int = 10, include_tags: list[str] | None = Query(default=None), exclude_tags: list[str] | None = Query(default=None)):
    prov = pick_provider()
    req = RecRequest(user_id=for_, limit=limit, include_tags=include_tags, exclude_tags=exclude_tags)
    items = await prov.search(q=None, limit=200)
    items = [i for i in items if keep(req, i)]
    items = items[: req.limit]
    if explain:
        return {"user_id": req.user_id, "source": getattr(prov, "name", "?"), "items": items, "family": {"strong_min_fit": [], "warning": "explain-mode stub"}}
    return items

