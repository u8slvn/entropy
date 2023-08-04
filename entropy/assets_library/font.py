from __future__ import annotations

from pathlib import Path

import pygame

from entropy.assets_library.assets_collection import AssetsCollection


class FontsCollection(AssetsCollection):
    def __init__(self) -> None:
        self.assets: dict[str, dict[str, pygame.font.Font]] = {}
        self._font_configs: list[tuple[Path, dict[str, int]]] = []

    def add_font(self, path: str | Path, **sizes: int) -> None:
        path = Path(path) if isinstance(path, str) else path
        self._font_configs.append((path, sizes))

    def get(self, name: str, size: str) -> pygame.font.Font:
        return self.assets[name][size]

    def load(self) -> None:
        for config in self._font_configs:
            file, sizes = config
            asset = {key: pygame.font.Font(file, size) for key, size in sizes.items()}
            self.assets[file.stem] = asset
