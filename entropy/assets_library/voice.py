from __future__ import annotations

import random

from collections import defaultdict
from pathlib import Path
from typing import ClassVar

import pygame as pg

from entropy.assets_library.assets_collection import AssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class VoicesCollection(AssetsCollection):
    extensions: ClassVar[list[str]] = [".wav"]

    def __init__(self, name: str):
        super().__init__(name=name)
        self._cache: dict[str, set[pg.mixer.Sound]] = defaultdict(set)
        self._files: dict[str, set[Path]] = defaultdict(set)

    def debug(self) -> None:
        logger.debug(
            f"{self._name.title()} library loaded with "
            f"{', '.join(self.extensions)} files:"
        )
        for voice, files in self._files.items():
            logger.debug(f'→ Voice "{voice}" found with {len(files)} file(s).')

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if not item.is_dir():
                continue

            for filepath in item.iterdir():
                if filepath.suffix not in self.extensions:
                    continue

                self._files[item.name].add(filepath)

    def _load_file(self, file: Path) -> pg.mixer.Sound:
        return pg.mixer.Sound(file)

    def get(self, name: str) -> pg.mixer.Sound:
        if self._cache.get(name) is None:
            self.load(name)

        return random.choice(list(self._cache[name]))

    def load(self, name: str | None = None) -> None:
        if name:
            for file in self._files[name]:
                self._cache[name].add(self._load_file(file=file))
        else:
            for name, files in self._files.items():
                for file in files:
                    self._cache[name].add(self._load_file(file=file))

    def preload(self, name: str) -> None:
        pass
