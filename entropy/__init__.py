from __future__ import annotations

import os

import pygame

from entropy.assets_library import AssetsLibrary
from entropy.config import Config
from entropy.gui.window import Window
from entropy.locations import ASSETS_DIR
from entropy.misc.control import Control
from entropy.misc.translator import Translator
from entropy.utils import Res


__all__ = ["assets", "window", "translator"]

config = Config()

window = Window(
    title="Entropy",
    render_res=Res(w=1920, h=1080),
    fullscreen=config.fullscreen,
)

translator = Translator(langs=["en", "fr"], default="en")

assets = AssetsLibrary()

control: Control


def init() -> None:
    global window, control, assets, translator

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()

    assets.fonts.add_font(path=ASSETS_DIR / "fonts/LanaPixel.ttf", small=20, big=40)
    assets.images.add_dir(path=ASSETS_DIR / "ui")
    assets.images.add_dir(path=ASSETS_DIR / "images")
    assets.sound.add_dir(path=ASSETS_DIR / "sound")
    assets.load()

    control = Control(fps=config.fps)


def start() -> None:
    global control

    control.start()
