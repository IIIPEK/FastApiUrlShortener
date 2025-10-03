# app/routers/shortener.py
from __future__ import annotations
import logging
import pathlib
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Url
from app.schemas.url import ShortenIn, ShortenOut
from app.services.shortener import to_base62, canonicalize_url
from app.core.config import settings

logger = logging.getLogger("app.router.shortener")
router = APIRouter(tags=["shortener"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ShortenOut)
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShortenOut)
async def create_short_url(payload: ShortenIn, db: Session = Depends(get_db)) -> ShortenOut:
    original = canonicalize_url(str(payload.url))
    logger.info("Incoming URL: %s | canonical: %s", payload.url, original)
    #logger.info("Database URL: %s", pathlib.Path(db.get_bind().url.database).resolve())

    row = db.scalar(select(Url).where(Url.original_url == original))
    if row:
        short = f"{settings.base_url.rstrip('/')}{settings.shortener_prefix}/{row.code}"
        return ShortenOut(id=row.code, short_url=short) # type: ignore[arg-type]
    try:
        row = Url(original_url=original)
        db.add(row)
        db.flush()
        row.code = to_base62(row.id)
        db.commit()
        db.refresh(row)
    except IntegrityError as e:
        logger.exception("IntegrityError on insert: %s", e)
        db.rollback()
        row = db.scalar(select(Url).where(Url.original_url == original))
        if not row:
            # highly unlikely, but possible if two requests race
            raise HTTPException(status_code=500, detail="Race condition on URL insert")

    short = f"{settings.base_url.rstrip('/')}{settings.shortener_prefix}/{row.code}"
    logger.info("Created short URL %s -> %s", row.code, row.original_url)
    return ShortenOut(id=row.code, short_url=short) # type: ignore[arg-type]

@router.post("/", include_in_schema=False)
async def create_short_url_with_slash(request: Request):
    logger.info("Incoming URL: %s\n Redirected to: %s", request.url, request.url.path.rstrip("/"))
    return RedirectResponse(
        url=request.url.path.rstrip("/"),
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
@router.get("/{code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def resolve_and_redirect(code: str, db: Session = Depends(get_db)):
    row = db.scalar(select(Url).where(Url.code == code))
    if not row:
        logger.info("Short URL not found: %s", code)
        raise HTTPException(status_code=404, detail="Short URL not found")
    logger.info("Redirecting %s -> %s", code, row.original_url)
    return RedirectResponse(url=row.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
