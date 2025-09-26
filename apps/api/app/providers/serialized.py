from fastapi import APIRouter

router = APIRouter(prefix="/providers/serialized", tags=["providers"])

@router.get("/ping")
def ping():
    return {"ok": True}

class SZ:
    def __init__(self):
        self.router = router
