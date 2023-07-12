from __future__ import annotations

import os

import pygame as pg

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import AssetsLibrary
from entropy.misc.game import Game


__all__ = ["assets", "game"]

assets: AssetsLibrary
game: Game


def init(title: str, fps: float, images_path: str) -> None:
    global game, assets

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pg.init()

    assets = AssetsLibrary()
    assets.fonts.add_font(
        path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40
    )
    assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    assets.images.add_dir(path=images_path)

    game = Game(
        title=title,
        fps=fps,
        render_resolution=(1920, 1080),
        fullscreen=False,
    )


def start() -> None:
    global game

    game.start()
