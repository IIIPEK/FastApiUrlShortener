# FastAPI URL Shortener

A compact, production-ready URL shortener built with **FastAPI**, **SQLAlchemy 2.x**, and **Pydantic v2**.  
Includes an async HTTP fetch endpoint and a clean test suite with `pytest`, `pytest-asyncio`, and `respx`.

## Features
- Create short links (`POST {SHORTENER_PREFIX}`) and resolve them with a **307 redirect** (`GET {SHORTENER_PREFIX}/{code}`).
- Idempotent create: posting the same original URL returns the existing code (unique on `original_url`).
- Async external fetch (`GET {FETCH_PREFIX}/fetch`) via `httpx.AsyncClient`.
- Config via `.env` using `pydantic-settings`.
- Solid project structure with routers/models/schemas/services, and async tests.

## Project layout
```
app/
  core/{config.py, logging_config.py}
  db/{base.py, session.py}
  models/{__init__.py, url.py}
  routers/{async_tasks.py, meta.py, shortener.py}
  schemas/url.py
  services/shortener.py
  deps.py
  main.py
tests/{conftest.py, test_fetch.py, test_health.py, test_shortener.py}
.env.example
pytest.ini
requirements.txt
LICENSE
```

## Requirements
See `requirements.txt`. Install:
```bash
pip install -r requirements.txt
```

## Configuration (.env)
Copy `.env.example` → `.env` and adjust if needed:
```
HOST=127.0.0.1
PORT=8080
BASE_URL=http://127.0.0.1:8080
DATABASE_URL=sqlite:///./data.db

SHORTENER_PREFIX=/u
FETCH_PREFIX=/api/fetch
```

## Run with built-in server wrapper
app can be launched with the command
``` bash
python run_server.py
```

## Run
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload --workers 1
```

## API
- Health: `GET /health`
- Create short URL: `POST {SHORTENER_PREFIX}`
- Resolve: `GET {SHORTENER_PREFIX}/{code}` → **307** redirect
- Async fetch: `GET {FETCH_PREFIX}/fetch?url=...`

## Testing
```bash
pytest -v
```
