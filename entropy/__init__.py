from __future__ import annotations

import os

import pygame

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import AssetsLibrary
from entropy.misc.game import Game
from entropy.misc.resolution import r900P, r1080P


__all__ = ["assets", "game"]

assets: AssetsLibrary
game: Game


def init(title: str, fps: float, images_path: str) -> None:
    global game, assets

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()

    assets = AssetsLibrary()
    assets.fonts.add_font(
        path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40
    )
    assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    assets.images.add_dir(path=images_path)

    game = Game(
        title=title,
        fps=fps,
        screen_resolution=r900P,
        max_resolution=r1080P,
        fullscreen=False,
    )


def start() -> None:
    global game

    game.start()
