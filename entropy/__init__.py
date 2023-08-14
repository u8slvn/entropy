from __future__ import annotations

import os

import pygame

from entropy import platform
from entropy.assets_library import AssetsLibrary
from entropy.config import get_config
from entropy.constants import GAME_NAME
from entropy.game.control import Control
from entropy.gui.mouse import Mouse
from entropy.gui.window import Window
from entropy.locations import ASSETS_DIR
from entropy.locations import USER_LOCAL_DIR
from entropy.logging import get_logger
from entropy.misc.translator import Translator
from entropy.mixer import Mixer
from entropy.utils import Res


__all__ = ["assets", "window", "translator", "mouse", "mixer"]

config = get_config()
logger = get_logger()

window: Window
mouse: Mouse
translator: Translator
assets: AssetsLibrary
control: Control
mixer = Mixer(
    main_vol=config.main_volume,
    music_vol=config.music_volume,
    atmos_vol=config.atmosphere_volume,
    voice_vol=config.voice_volume,
    uisfx_vol=config.uisfx_volume,
)


def init() -> None:
    global window, mouse, translator, assets, control

    logger.info(f"Initialize {GAME_NAME}.")

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    platform.configure()

    USER_LOCAL_DIR.mkdir(exist_ok=True)

    pygame.init()

    window = Window(
        title=GAME_NAME.title(),
        default_res=Res(w=1920, h=1080),
        fullscreen=config.fullscreen,
    )
    mouse = Mouse()
    translator = Translator(locales=["en", "fr"], locale=config.locale)

    assets = AssetsLibrary()
    assets.fonts.add_font(
        path=ASSETS_DIR / "fonts/LanaPixel.ttf",
        small=22,
        medium=33,
        big=44,
        settings=55,
    )
    assets.images.add_dir(path=ASSETS_DIR / "gui")
    assets.images.add_dir(path=ASSETS_DIR / "images")
    assets.sound.add_dir(path=ASSETS_DIR / "sound")
    assets.sound.add_dir(path=ASSETS_DIR / "music")
    assets.load()

    control = Control(fps=config.fps)


def start() -> None:
    global control

    control.start()
