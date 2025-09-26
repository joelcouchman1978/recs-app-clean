from fastapi import APIRouter

router = APIRouter(prefix="/providers/justwatch", tags=["providers"])

@router.get("/ping")
def ping():
    return {"ok": True}

class JW:
    def __init__(self):
        self.router = router
