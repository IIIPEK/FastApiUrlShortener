# app/models/url.py
from __future__ import annotations
from datetime import datetime,timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, UniqueConstraint
from typing import Optional
from app.db.base import Base

class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[Optional[str]] = mapped_column(String(16), unique=True, index=True, nullable=True)
    original_url: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("code", name="uq_urls_code"),
        UniqueConstraint("original_url", name="uq_urls_original_url"),
    )
