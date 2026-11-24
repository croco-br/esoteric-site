"""Content-fingerprinted static asset URLs for safe long-lived caching."""

from hashlib import blake2s
from pathlib import Path


def fingerprinted(static_dir: Path, route_name: str):
    """Build a template global `static_url(request, path)` adding a ?v= content digest."""
    def static_url(request, path: str) -> str:
        digest = blake2s((static_dir / path).read_bytes(), digest_size=8).hexdigest()
        return f"{request.url_for(route_name, path=path)}?v={digest}"
    return static_url
