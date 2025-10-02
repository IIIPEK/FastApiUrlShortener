# app/routers/meta.py
from __future__ import annotations
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["meta"])

@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}