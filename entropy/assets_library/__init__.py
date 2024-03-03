from __future__ import annotations

from entropy.assets_library.font import FontsCollection
from entropy.assets_library.image import ImagesCollection
from entropy.assets_library.sound import SoundsCollection
from entropy.assets_library.voice import VoicesCollection


class AssetsLibrary:
    def __init__(self) -> None:
        self.font = FontsCollection()
        self.image = ImagesCollection()
        self.sound = SoundsCollection()
        self.voice = VoicesCollection()

    def load(self) -> None:
        self.font.load()
        self.font.debug()

        self.image.load()
        self.image.debug()

        self.sound.load()
        self.sound.debug()

        self.voice.load()
        self.voice.debug()
