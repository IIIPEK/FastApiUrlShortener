# app/db/session.py
from __future__ import annotations
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from .base import Base
from app.core.config import settings

logger = logging.getLogger("app.db.session")

db_url = settings.database_url

engine = create_engine(db_url, echo=False, future=True)
#logger.info("DB URL in use: %s", engine.url.render_as_string(hide_password=False))

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)

def init_db() -> None:
    # Import models so that they register with Base, then create tables
    # Импортируем модели, чтобы они зарегистрировались в Base, затем создаём таблицы
    from app import models # noqa: F401
    logger.info("DB URL in use: %s", db_url)
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        try:
            cols = conn.execute(text("PRAGMA table_info(urls);")).all()
            #logger.info("PRAGMA table_info(urls): %s", cols)
        except Exception as e:
            logger.warning("PRAGMA failed (table may not exist yet): %s", e)
