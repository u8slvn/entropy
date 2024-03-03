from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pygame

from entropy.assets_library.assets_collection import DirAssetsCollection
from entropy.logging import get_logger


logger = get_logger()


class SoundsCollection(DirAssetsCollection):
    extensions: ClassVar[list[str]] = [".wav", ".ogg"]

    def debug(self) -> None:
        logger.debug(
            f"Sound library loaded with \"{', '.join(self.extensions)}\" files:"
        )
        logger.debug(f'→ "{len(self.assets)}" file(s) found.')

    def _load_file(self, file: Path) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(file)
