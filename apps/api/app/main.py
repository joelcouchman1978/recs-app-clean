from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AU TV Recommender API", version="0.1.0")

class RecRequest(BaseModel):
    user_id: str | None = None
    limit: int = 10

@app.get("/readyz")
def readyz():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/recommendations")
def recommendations(req: RecRequest):
    items = [f"show_{i}" for i in range(req.limit)]
    return {"user_id": req.user_id, "items": items}
