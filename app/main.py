# app/main.py
from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import init_db
from app.routers import meta, shortener, async_tasks



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="URL Shortener", version="1.0.0", lifespan=lifespan )

# Routers
app.include_router(meta.router)
app.include_router(shortener.router)
app.include_router(async_tasks.router)

# Dev entrypoint (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=True,
            log_level="info",
    )
