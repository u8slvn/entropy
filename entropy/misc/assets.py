from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from pathlib import Path
from typing import Any

import pygame.font


class AssetsManager(ABC):
    extensions: list[str]

    def __init__(self) -> None:
        self._files: deque[Path] = deque()
        self.assets: dict[str, Any] = {}

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files.append(item)

    @property
    def nb_files(self) -> int:
        return len(self._files)

    @abstractmethod
    def cast(self, file: Path) -> Any:
        ...

    def load(self) -> None:
        self.assets.update({file.stem: self.cast(file) for file in self._files})


class FontsManager(AssetsManager):
    extensions = [".ttf"]

    def cast(self, file: Path) -> Any:
        return file

    def get(self, name: str, size: int) -> pygame.font.Font:
        return pygame.font.Font(self.assets[name], size)


class ImagesManager(AssetsManager):
    extensions = [".png"]
    alpha_suffix = "-a"

    def cast(self, file: Path) -> Any:
        if file.stem.endswith(self.alpha_suffix):
            return pygame.image.load(file).convert_alpha()

        return pygame.image.load(file).convert()

    def get(self, name: str) -> pygame.Surface:
        return self.assets[name]


class Assets:
    def __init__(self):
        self.fonts = FontsManager()
        self.images = ImagesManager()

    def load(self) -> None:
        self.fonts.load()
        self.images.load()
