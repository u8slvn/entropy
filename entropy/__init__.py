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
from entropy.locations import LOCALES_DIR
from entropy.locations import USER_LOCAL_DIR
from entropy.logging import get_logger
from entropy.mixer import Mixer
from entropy.translator import Translator
from entropy.utils.measure import Res


__all__ = ["assets", "window", "translator", "mouse", "mixer"]

config = get_config()
logger = get_logger()

window: Window
mouse: Mouse
translator: Translator
assets: AssetsLibrary
control: Control
mixer: Mixer


def init() -> None:
    global window, mouse, translator, assets, control, mixer

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
    translator = Translator(localedir=LOCALES_DIR, locale=config.locale)

    assets = AssetsLibrary()
    assets.font.add_font(
        path=ASSETS_DIR / "fonts/LanaPixel.ttf",
        xs=22,
        sm=33,
        md=44,
        lg=55,
        xl=66,
        xxl=77,
        xxxl=88,
    )
    assets.gui.add_dir(path=ASSETS_DIR / "gui")
    assets.guisfx.add_dir(path=ASSETS_DIR / "guisfx")
    assets.sound.add_dir(path=ASSETS_DIR / "musics")
    assets.sound.add_dir(path=ASSETS_DIR / "sounds")
    assets.image.add_dir(path=ASSETS_DIR / "images")
    assets.voice.add_dir(path=ASSETS_DIR / "voices")
    assets.load()

    mixer = Mixer(
        main_vol=config.main_volume,
        music_vol=config.music_volume,
        atmos_vol=config.atmosphere_volume,
        voice_vol=config.voice_volume,
        uisfx_vol=config.uisfx_volume,
    )

    control = Control(fps=config.fps)


def start(state: str = "Splash") -> None:
    global control

    control.start(state=state)
