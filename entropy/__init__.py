from __future__ import annotations

import pygame

from entropy import logger
from entropy.assets_library import AssetsLibrary
from entropy.compat import configure_display
from entropy.gui.mouse import Mouse
from entropy.gui.window import Window
from entropy.locations import ASSETS_DIR
from entropy.misc.config import Config
from entropy.misc.control import Control
from entropy.misc.translator import Translator
from entropy.utils import Res


__all__ = ["assets", "config", "window", "translator", "mouse"]

config: Config
window: Window
mouse: Mouse
translator: Translator
assets: AssetsLibrary
control: Control


def init() -> None:
    global config, window, mouse, translator, assets, control

    configure_display()
    logger.configure()

    pygame.init()

    config = Config()
    window = Window(
        title="Entropy",
        default_res=Res(w=1920, h=1080),
        fullscreen=config.fullscreen,
    )
    mouse = Mouse()
    translator = Translator(locales=["en", "fr"], locale="en")

    assets = AssetsLibrary()
    assets.fonts.add_font(
        path=ASSETS_DIR / "fonts/LanaPixel.ttf", small=22, big=44, settings=55
    )
    assets.images.add_dir(path=ASSETS_DIR / "gui")
    assets.images.add_dir(path=ASSETS_DIR / "images")
    assets.sound.add_dir(path=ASSETS_DIR / "sound")
    assets.load()

    control = Control(fps=config.fps)


def start() -> None:
    global control

    control.start()
