# app/services/shortener.py
from __future__ import annotations
import string
from urllib.parse import urlsplit, urlunsplit

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def to_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]
    base = 62
    digits: list[str] = []
    while num:
        num, rem = divmod(num, base)
        digits.append(BASE62_ALPHABET[rem])
    return "".join(reversed(digits))

def canonicalize_url(u: str) -> str:
    parts = urlsplit(u)
    # domain to lovercase; remove empty path -> '/'
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    # remove final "/"
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((parts.scheme, netloc, path, parts.query, parts.fragment))