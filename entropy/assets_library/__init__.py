from __future__ import annotations

from entropy.assets_library.font import FontsCollection
from entropy.assets_library.image import ImagesCollection
from entropy.assets_library.sound import SoundCollection


class AssetsLibrary:
    def __init__(self) -> None:
        self.fonts = FontsCollection()
        self.images = ImagesCollection()
        self.sound = SoundCollection()

    def load(self) -> None:
        self.fonts.load()
        self.images.load()
        self.sound.load()
