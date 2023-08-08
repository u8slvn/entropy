from __future__ import annotations

import os

import pygame

from entropy.assets_library import AssetsLibrary
from entropy.gui.mouse import Mouse
from entropy.gui.window import Window
from entropy.locations import ASSETS_DIR
from entropy.locations import CONFIG_FILE_PATH
from entropy.locations import USER_LOCAL_DIR
from entropy.logging import logger
from entropy.misc.config import Config
from entropy.misc.control import Control
from entropy.misc.translator import Translator
from entropy.utils import Res


__all__ = ["assets", "config", "window", "translator", "mouse", "logger"]

logger = logger()

config: Config
window: Window
mouse: Mouse
translator: Translator
assets: AssetsLibrary
control: Control


def init() -> None:
    global config, window, mouse, translator, assets, control

    logger.info("Initialize entropy.")

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    USER_LOCAL_DIR.mkdir(exist_ok=True)

    pygame.init()

    config = Config(config_file=CONFIG_FILE_PATH)
    window = Window(
        title="Entropy",
        default_res=Res(w=1920, h=1080),
        fullscreen=config.fullscreen,
    )
    mouse = Mouse()
    translator = Translator(locales=["en", "fr"], locale=config.locale)

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
