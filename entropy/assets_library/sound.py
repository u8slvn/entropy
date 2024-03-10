from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pygame as pg

from entropy.assets_library.assets_collection import DirAssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class SoundsCollection(DirAssetsCollection[pg.mixer.Sound]):
    extensions: ClassVar[list[str]] = [".wav", ".ogg"]

    def debug(self) -> None:
        logger.debug(
            f"{self._name.title()} library loaded with "
            f"\"{', '.join(self.extensions)}\" files:"
        )
        logger.debug(f"→ {len(self._files)} file(s) found.")

    def _load_file(self, file: Path) -> pg.mixer.Sound:
        return pg.mixer.Sound(file)
