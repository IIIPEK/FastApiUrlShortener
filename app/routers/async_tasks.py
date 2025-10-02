# app/routers/async_tasks.py
from __future__ import annotations
import httpx
from fastapi import APIRouter, Query
from pydantic import AnyHttpUrl

router = APIRouter(tags=["async"])

@router.get("/fetch")
async def async_fetch(url: AnyHttpUrl = Query(...), timeout: float = Query(5.0, gt=0)) -> dict:
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        r = await client.get(str(url))
        body_text = r.text
        if len(body_text) > 4096:
            body_text = body_text[:4096] + "…[truncated]"
        return {
            "status_code": r.status_code,
            "headers": dict(r.headers),
            "url": str(r.url),
            "elapsed_ms": r.elapsed.total_seconds() * 1000.0,
            "body": body_text,
        }
