from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pygame as pg

from entropy.assets_library.assets_collection import DirAssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class ImagesCollection(DirAssetsCollection[pg.Surface]):
    extensions: ClassVar[list[str]] = [".png"]
    alpha_suffix = "-a"

    def debug(self) -> None:
        logger.debug(
            f"{self._name.title()} library loaded with"
            f"\"{', '.join(self.extensions)}\" files:"
        )
        logger.debug(f"→ {len(self._files)} file(s) found.")

    def _load_file(self, file: Path) -> pg.Surface:
        if file.stem.endswith(self.alpha_suffix):
            return pg.image.load(file).convert_alpha()
        else:
            return pg.image.load(file).convert()
