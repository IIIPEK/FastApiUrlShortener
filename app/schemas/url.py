# app/schemas/url.py
from __future__ import annotations
from pydantic import BaseModel, AnyHttpUrl

class ShortenIn(BaseModel):
    url: AnyHttpUrl

class ShortenOut(BaseModel):
    id: str
    short_url: AnyHttpUrl
