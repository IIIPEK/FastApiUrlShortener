# tests/test_health.py
from __future__ import annotations
import pytest

pytestmark = pytest.mark.asyncio

async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "time" in data
