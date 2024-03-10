from __future__ import annotations

from pathlib import Path

import pygame as pg

from entropy.assets_library.assets_collection import AssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class FontsCollection(AssetsCollection):
    def __init__(self, name: str):
        super().__init__(name=name)
        self._cache: dict[str, dict[str, pg.font.Font]] = {}
        self._font_configs: dict[str, tuple[Path, dict[str, int]]] = {}

    def debug(self) -> None:
        logger.debug(f"{self._name.title()} library loaded:")
        for font, configs in self._cache.items():
            logger.debug(f'→ Font "{font}" found with {len(configs)} config(s).')

    def add_font(self, path: str | Path, **sizes: int) -> None:
        path = Path(path) if isinstance(path, str) else path
        self._font_configs[path.stem] = (path, sizes)

    def get(self, name: str, size: str) -> pg.font.Font:
        return self._cache[name][size]

    def load(self, name: str | None = None) -> None:
        configs = self._font_configs[name] if name else self._font_configs.values()
        print(self._font_configs)
        for config in configs:
            file, sizes = config
            asset = {key: pg.font.Font(file, size) for key, size in sizes.items()}
            self._cache[file.stem] = asset

    def preload(self, name: str) -> None:
        pass
