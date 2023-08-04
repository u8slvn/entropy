from __future__ import annotations

from pathlib import Path

import pygame

from entropy.assets_library.assets_collection import DirAssetsCollection


class ImagesCollection(DirAssetsCollection):
    extensions = [".png"]
    alpha_suffix = "-a"

    def _load_file(self, file: Path) -> pygame.Surface:
        if file.stem.endswith(self.alpha_suffix):
            return pygame.image.load(file).convert_alpha()
        else:
            return pygame.image.load(file).convert()
