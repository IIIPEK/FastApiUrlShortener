# app/db/session.py
from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .base import Base
from app.core.config import settings

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)

def init_db() -> None:
    # Import models so that they register with Base, then create tables
    # Импортируем модели, чтобы они зарегистрировались в Base, затем создаём таблицы
    from app import models # noqa: F401
    Base.metadata.create_all(engine)