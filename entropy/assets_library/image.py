from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pygame

from entropy.assets_library.assets_collection import DirAssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class ImagesCollection(DirAssetsCollection):
    extensions: ClassVar[list[str]] = [".png"]
    alpha_suffix = "-a"

    def debug(self) -> None:
        logger.debug(
            f"Sound library loaded with \"{', '.join(self.extensions)}\" files:"
        )
        logger.debug(f'→ "{len(self.assets)}" file(s) found.')

    def _load_file(self, file: Path) -> pygame.Surface:
        if file.stem.endswith(self.alpha_suffix):
            return pygame.image.load(file).convert_alpha()
        else:
            return pygame.image.load(file).convert()
