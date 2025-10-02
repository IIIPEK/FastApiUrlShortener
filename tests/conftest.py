# tests/conftest.py
from __future__ import annotations
import os
import pathlib
import tempfile
import pytest
import httpx
from httpx import ASGITransport

# 1) Ставим env ДО импорта приложения (DB в отдельный временный файл)
@pytest.fixture(scope="session", autouse=True)
def _env_setup():
    tmpdir = tempfile.TemporaryDirectory()
    db_path = pathlib.Path(tmpdir.name) / "test.db"
    os.environ.setdefault("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    os.environ.setdefault("BASE_URL", "http://testserver")
    os.environ.setdefault("HOST", "127.0.0.1")
    os.environ.setdefault("PORT", "8080")

    yield  # тесты выполняются

    # 4) Гарантированно закрываем соединения и удаляем tmpdir
    try:
        from app.db.session import engine
        engine.dispose()  # снимаем file-lock с SQLite на Windows
    except Exception:
        pass
    tmpdir.cleanup()

# 2) Импортируем приложение (после установки env)
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
