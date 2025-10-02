# app/routers/shortener.py
from __future__ import annotations
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
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

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShortenOut)
async def create_short_url(payload: ShortenIn, db: Session = Depends(get_db)) -> ShortenOut:
    original = canonicalize_url(str(payload.url))
    logger.info("Incoming URL: %s | canonical: %s", payload.url, original)

    row = db.scalar(select(Url).where(Url.original_url == original))
    if row:
        short = f"{settings.base_url.rstrip('/')}/{row.code}"
        return ShortenOut(id=row.code, short_url=short) # type: ignore[arg-type]
    try:
        row = Url(original_url=original)
        db.add(row)
        db.flush()
        row.code = to_base62(row.id)
        db.commit()
        db.refresh(row)
    except IntegrityError:
        db.rollback()
        row = db.scalar(select(Url).where(Url.original_url == original))
        if not row:
            # highly unlikely, but possible if two requests race
            raise HTTPException(status_code=500, detail="Race condition on URL insert")

    short = f"{settings.base_url.rstrip('/')}/{row.code}"
    logger.info("Created short URL %s -> %s", row.code, row.original_url)
    return ShortenOut(id=row.code, short_url=short) # type: ignore[arg-type]

@router.get("/{code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def resolve_and_redirect(code: str, db: Session = Depends(get_db)):
    row = db.scalar(select(Url).where(Url.code == code))
    if not row:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=row.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)