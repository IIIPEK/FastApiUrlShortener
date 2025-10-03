# app/routers/async_tasks.py
from __future__ import annotations
import httpx
import logging
from fastapi import APIRouter, Query, HTTPException
from pydantic import AnyHttpUrl

logger = logging.getLogger("app.router.async_tasks")
router = APIRouter(tags=["async"])

@router.get("/fetch/")
@router.get("/fetch")
async def async_fetch(url: AnyHttpUrl = Query(...), timeout: float = Query(5.0, gt=0)) -> dict:
    async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    ) as client:
        logger.info("Fetching %s", url)
        try:
            r = await client.get(str(url))
            r.raise_for_status()
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
        except httpx.TimeoutException:
            logger.warning("Timeout fetching %s", url)
            raise HTTPException(status_code=504, detail="Request timeout")
        except httpx.HTTPStatusError as e:
            logger.warning("HTTP error %s: %s", e.response.status_code, url)
            return {
                "status_code": e.response.status_code,
                "headers": dict(e.response.headers),
                "url": str(e.response.url),
                "elapsed_ms": e.response.elapsed.total_seconds() * 1000.0,
                "body": e.response.text,
            }
        except httpx.RequestError as e:
            logger.warning("Request error: %s", e)
            raise HTTPException(status_code=502, detail=f"Request failed: {str(e)}")

