from __future__ import annotations

import os

import pygame

from entropy.locations import ASSETS_DIR
from entropy.misc.game import Game
from entropy.misc.resolution import r900P, r1080P


game: Game


def init(title: str, fps: float, images_path: str) -> None:
    global game

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()

    game = Game(
        title=title,
        fps=fps,
        screen_resolution=r900P,
        max_resolution=r1080P,
        fullscreen=False,
    )

    game.assets.fonts.add_font(
        path=ASSETS_DIR.joinpath("fonts/LanaPixel.ttf"), small=20, big=40
    )

    game.assets.images.add_dir(path=ASSETS_DIR.joinpath("gui"))
    game.assets.images.add_dir(path=images_path)


def start() -> None:
    global game

    game.start()
