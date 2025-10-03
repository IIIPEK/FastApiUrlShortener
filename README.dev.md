# Developer Notes

## Stack & Decisions
- **FastAPI** for routing and DI
- **SQLAlchemy 2.x** ORM with session dependency
- **Pydantic v2** & `pydantic-settings`
- **httpx.AsyncClient** for outbound HTTP
- Idempotent logic with unique constraints

## URL Model
- `code: Optional[str]` (nullable, unique, indexed)
- `original_url: str` unique
- Insertion flow: find-or-create with flush/commit and IntegrityError handling

## Routing
- Shortener:
  - `POST {SHORTENER_PREFIX}` create
  - `POST {SHORTENER_PREFIX}/` → 307 redirect
  - `GET {SHORTENER_PREFIX}/{code}` → 307 Location
- Fetch:
  - `GET {FETCH_PREFIX}/fetch`

## Settings
Loaded from `.env`. Be careful: env is read at import time.

## SQLite Tips
- Use absolute paths
- Delete DB file when schema changes in dev
- On Windows: keep workers=1

## Testing
- `pytest` + `pytest-asyncio`
- `respx` for HTTP mocks
- `ASGITransport` for in-process tests

## Makefile (optional)
```
run:
	uvicorn app.main:app --reload

test:
	pytest -q
```
