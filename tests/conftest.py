# tests/conftest.py
from __future__ import annotations
import os
import pathlib
import pytest
import tempfile
import httpx
from httpx import ASGITransport

@pytest.fixture(scope="session", autouse=True)
def _env_setup():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = pathlib.Path(tmpdir) / "test.db"
        os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path}")
        os.environ.setdefault("BASE_URL", "http://testserver")
        os.environ.setdefault("HOST", "127.0.0.1")
        os.environ.setdefault("PORT", "8080")
        yield

@pytest.fixture(scope="session")
def app_instance():
    # Импорт после установки env
    from app.main import app
    return app

@pytest.fixture
async def client(app_instance):
    transport = ASGITransport(app=app_instance, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
