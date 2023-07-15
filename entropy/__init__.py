from __future__ import annotations

import os

import pygame as pg

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import AssetsLibrary
from entropy.misc.control import Control
from entropy.misc.translator import Translator
from entropy.misc.window import Window
from entropy.states import States


__all__ = ["assets", "control"]

from entropy.utils import Resolution


assets: AssetsLibrary
control: Control
translator: Translator


def init(title: str, fps: float, images_path: str) -> None:
    global control, assets, translator

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pg.init()

    window = Window(
        title=title,
        render_resolution=Resolution(w=1920, h=1080),
        fullscreen=False,
    )

    translator = Translator(langs=["en", "fr"], default="en")

    assets = AssetsLibrary()
    assets.fonts.add_font(path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40)
    assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    assets.images.add_dir(path=images_path)
    assets.sound.add_dir(path=ASSETS_DIR.joinpath("sound"))
    assets.load()

    control = Control(
        window=window,
        fps=fps,
        states=States.load(),
        state="SPLASH",
    )


def start() -> None:
    global control

    control.start()
