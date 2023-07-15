from __future__ import annotations

import os

import pygame as pg

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import AssetsLibrary
from entropy.misc.control import Control
from entropy.misc.translator import Translator
from entropy.misc.window import Window
from entropy.utils import Resolution


__all__ = ["assets", "window", "translator"]

window: Window
assets: AssetsLibrary
control: Control
translator: Translator


def init(title: str, fps: float, images_path: str) -> None:
    global window, control, assets, translator

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pg.init()

    window = Window(
        title=title,
        render_res=Resolution(w=1920, h=1080),
        fullscreen=False,
    )

    translator = Translator(langs=["en", "fr"], default="en")

    assets = AssetsLibrary()
    assets.fonts.add_font(path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40)
    assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    assets.images.add_dir(path=images_path)
    assets.sound.add_dir(path=ASSETS_DIR.joinpath("sound"))
    assets.load()

    control = Control(fps=fps)


def start() -> None:
    global control

    control.start()
