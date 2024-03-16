from __future__ import annotations

from entropy.assets_library.cache import get_cache


def test_assets_cache():
    cache = get_cache()
    cache.set("test", "key", "value")

    assert cache.get("test", "key") == "value"

    cache.clear("test", "key")

    assert cache.get("test", "key") is None

    cache.set("test", "key1", "value1")
    cache.set("test", "key2", "value2")

    cache.clear_keys("test", "key1", "key2")

    assert cache.get("test", "key1") is None
    assert cache.get("test", "key2") is None
