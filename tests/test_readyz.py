import httpx, asyncio
async def _get(url): 
    async with httpx.AsyncClient() as c: 
        r = await c.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
def test_readyz_shape():
    data = asyncio.run(_get("http://127.0.0.1:8000/readyz"))
    assert data.get("status") == "ok"
