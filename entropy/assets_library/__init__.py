from __future__ import annotations

from entropy.assets_library.font import FontsCollection
from entropy.assets_library.image import ImagesCollection
from entropy.assets_library.sound import SoundsCollection
from entropy.assets_library.voice import VoicesCollection


class AssetsLibrary:
    def __init__(self) -> None:
        self.font = FontsCollection("font")
        self.gui = ImagesCollection("gui")
        self.guisfx = SoundsCollection("guisfx")
        self.image = ImagesCollection("image")
        self.sound = SoundsCollection("sound")
        self.voice = VoicesCollection("voice")

    def load(self) -> None:
        self.font.load()
        self.font.debug()
        self.gui.load()
        self.gui.debug()
        self.guisfx.load()
        self.guisfx.debug()
        self.image.load()
        self.image.debug()
        self.sound.load()
        self.sound.debug()
        self.voice.load()
        self.voice.debug()
