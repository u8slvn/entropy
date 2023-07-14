from __future__ import annotations

import os

import pygame as pg

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import AssetsLibrary
from entropy.misc.control import Control
from entropy.misc.window import Window
from entropy.states import States


__all__ = ["assets", "control"]

assets: AssetsLibrary
control: Control


def init(title: str, fps: float, images_path: str) -> None:
    global control, assets

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pg.init()

    window = Window(
        title=title,
        render_resolution=(1920, 1080),
        fullscreen=False,
    )

    assets = AssetsLibrary()
    assets.fonts.add_font(
        path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40
    )
    assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    assets.images.add_dir(path=images_path)
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
