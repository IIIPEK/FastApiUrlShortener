# tests/test_shortener.py
from __future__ import annotations
import pytest


pytestmark = pytest.mark.asyncio

async def test_create_and_redirect(client):
    from app.core.config import settings
    original = "https://example.com/long/path?q=1"

    # create short link
    r = await client.post(f"{settings.shortener_prefix}", json={"url": original}, follow_redirects=True)
    assert r.status_code == 201
    payload = r.json()
    assert "id" in payload and payload["id"]

    code = payload["id"]

    assert payload["short_url"].endswith(f"{settings.shortener_prefix}/{code}")

    # Test redirect (without following the redirect)
    r2 = await client.get(f"{settings.shortener_prefix}/{code}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers.get("location") == original