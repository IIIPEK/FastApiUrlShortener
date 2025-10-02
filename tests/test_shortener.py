# tests/test_shortener.py
from __future__ import annotations

async def test_create_and_redirect(client):
    original = "https://example.com/long/path?q=1"

    # create short link
    r = await client.post("/", json={"url": original})
    assert r.status_code == 201
    payload = r.json()
    assert "id" in payload and payload["id"]
    assert payload["short_url"].startswith("http://testserver/")


    code = payload["id"]

    # Test redirect (without following the redirect)
    r2 = await client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers.get("location") == original