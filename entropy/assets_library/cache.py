from __future__ import annotations

from collections import defaultdict
from contextlib import suppress
from typing import Any


_cache: _AssetsCache | None = None


class _AssetsCache:
    """Centralized cache for assets."""

    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = defaultdict(dict)

    def get(self, cache_name: str, key: str) -> Any:
        """Get an asset from the cache."""
        try:
            return self._cache[cache_name][key]
        except KeyError:
            return None

    def set(self, cache_name: str, key: str, value: Any) -> None:
        """Set an asset in the cache."""
        self._cache[cache_name][key] = value

    def clear(self, cache_name: str, key: str) -> None:
        """Clear an asset from the cache."""
        with suppress(KeyError):
            del self._cache[cache_name][key]

    def clear_keys(self, cache_name: str, *keys: str) -> None:
        """Clear multiple assets from the cache."""
        for key in keys:
            self.clear(cache_name, key)


def get_cache() -> _AssetsCache:
    """Return the assets cache."""
    global _cache

    if _cache is None:
        _cache = _AssetsCache()

    return _cache
