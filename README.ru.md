# Сокращатель ссылок на FastAPI

Лёгкий сервис сокращения ссылок на **FastAPI** + **SQLAlchemy 2.x** + **Pydantic v2**.  
Есть асинхронный эндпоинт для HTTP-запросов вовне и набор автотестов (`pytest`, `pytest-asyncio`, `respx`).

## Возможности
- Создание короткой ссылки (`POST {SHORTENER_PREFIX}`) и переход на оригинал с **307** (`GET {SHORTENER_PREFIX}/{code}`).
- Идемпотентное создание: повторный POST того же URL возвращает существующий код.
- Асинхронный фетч внешнего URL: `GET {FETCH_PREFIX}/fetch`.
- Конфигурация через `.env`.

## Структура проекта
```
app/…
tests/…
.env.example
pytest.ini
requirements.txt
LICENSE
```

## Зависимости
Установка:
```bash
pip install -r requirements.txt
```

## Настройки (.env)
```
HOST=127.0.0.1
PORT=8080
BASE_URL=http://127.0.0.1:8080
DATABASE_URL=sqlite:///./data.db

SHORTENER_PREFIX=/u
FETCH_PREFIX=/api/fetch
```
## Запуск через обертку встроенного сервера
Приложение можно поднять командой
``` bash
python run_server.py
```
## Запуск через uvicorn
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload --workers 1
```

## Эндпоинты
- Здоровье: `GET /health`
- Создание: `POST {SHORTENER_PREFIX}`
- Редирект: `GET {SHORTENER_PREFIX}/{code}`
- Фетч: `GET {FETCH_PREFIX}/fetch?url=...`

## Тесты
```bash
pytest -v
```
