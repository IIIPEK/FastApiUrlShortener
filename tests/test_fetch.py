# tests/test_fetch.py
from __future__ import annotations
import respx
import httpx

@respx.mock
async def test_fetch_mocks_external_http(client):
    test_url = "https://example.com/"
    respx.get(test_url).mock(return_value=httpx.Response(200, text="hello"))

    r = await client.get("/fetch", params={"url": test_url})
    assert r.status_code == 200
    data = r.json()
    assert data["status_code"] == 200
    assert data["url"].startswith(test_url)
    assert "hello" in data["body"]