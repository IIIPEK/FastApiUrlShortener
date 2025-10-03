# tests/conftest.py
from __future__ import annotations

import os, tempfile, pathlib, atexit
_tmpdir = tempfile.TemporaryDirectory()
_db_path = pathlib.Path(_tmpdir.name) / "test.db"

os.environ.setdefault("DATABASE_URL", f"sqlite:///{_db_path.as_posix()}")
os.environ.setdefault("BASE_URL", "http://testserver")
os.environ.setdefault("HOST", "127.0.0.1")
os.environ.setdefault("PORT", "8080")
print("TEST DB PATH:", _db_path.as_posix())
@atexit.register
def _cleanup():
    # аккуратно снимаем локи с SQLite и чистим каталог
    try:
        from app.db.session import engine
        engine.dispose()
    except Exception:
        pass
    _tmpdir.cleanup()

import pytest
import httpx
from httpx import ASGITransport

@pytest.fixture(scope="session")
def app_instance():
    from app.main import app
    # 3) Жестко убеждаемся, что таблицы созданы
    from app.db.session import init_db
    init_db()
    return app

# 5) httpx 0.28+: без lifespan-параметра — он уже управляется автоматически
@pytest.fixture
async def client(app_instance):
    transport = ASGITransport(app=app_instance)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c
