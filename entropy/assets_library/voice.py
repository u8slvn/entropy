from __future__ import annotations

import random

from collections import defaultdict
from pathlib import Path
from typing import ClassVar

import pygame

from entropy.assets_library.assets_collection import AssetsCollection


class VoicesCollection(AssetsCollection):
    extensions: ClassVar[list[str]] = [".wav"]

    def __init__(self) -> None:
        self.assets: dict[str, list[pygame.mixer.Sound]] = defaultdict(list)
        self._files: dict[str, list[Path]] = defaultdict(list)

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if not item.is_dir():
                continue

            for filepath in item.iterdir():
                if filepath.suffix not in self.extensions:
                    continue

                self._files[item.name].append(filepath)

    def _load_file(self, file: Path) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(file)

    def get(self, name: str) -> pygame.mixer.Sound:
        return random.choice(self.assets[name])

    def load(self) -> None:
        for voice, files in self._files.items():
            for file in files:
                self.assets[voice].append(self._load_file(file=file))
