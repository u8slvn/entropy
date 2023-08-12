from __future__ import annotations

from pathlib import Path

import pygame

from entropy.assets_library.assets_collection import DirAssetsCollection


class SoundCollection(DirAssetsCollection):
    extensions = [".wav", ".ogg"]

    def _load_file(self, file: Path) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(file)
