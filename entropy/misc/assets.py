from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any

import pygame as pg


class AssetsCollection(ABC):
    @abstractmethod
    def load(self) -> None:
        ...


class DirAssetsCollection(AssetsCollection, ABC):
    extensions: list[str]

    def __init__(self) -> None:
        self.assets: dict[str, Any] = {}
        self._files: list[Path] = []

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files.append(item)

    @abstractmethod
    def _load_file(self, file: Path) -> Any:
        ...

    def load(self) -> None:
        for file in self._files:
            self.assets[file.stem] = self._load_file(file=file)

    def get(self, name: str) -> Any:
        return self.assets[name]


class ImagesCollection(DirAssetsCollection):
    extensions = [".png"]
    alpha_suffix = "-a"

    def _load_file(self, file: Path) -> pg.Surface:
        if file.stem.endswith(self.alpha_suffix):
            return pg.image.load(file).convert_alpha()
        else:
            return pg.image.load(file).convert()


class SoundCollection(DirAssetsCollection):
    extensions = [".wav"]

    def _load_file(self, file: Path) -> pg.mixer.Sound:
        return pg.mixer.Sound(file)


class FontsCollection(AssetsCollection):
    def __init__(self) -> None:
        self.assets: dict[str, dict[str, pg.font.Font]] = {}
        self._font_configs: list[tuple[Path, dict[str, int]]] = []

    def add_font(self, path: str | Path, **sizes: int) -> None:
        path = Path(path) if isinstance(path, str) else path
        self._font_configs.append((path, sizes))

    def get(self, name: str, size: str) -> pg.font.Font:
        return self.assets[name][size]

    def load(self) -> None:
        for config in self._font_configs:
            file, sizes = config
            asset = {key: pg.font.Font(file, size) for key, size in sizes.items()}
            self.assets[file.stem] = asset


class AssetsLibrary:
    def __init__(self) -> None:
        self.fonts = FontsCollection()
        self.images = ImagesCollection()
        self.sound = SoundCollection()

    def load(self) -> None:
        self.fonts.load()
        self.images.load()
        self.sound.load()
