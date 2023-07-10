from __future__ import annotations

import os

import pygame

from entropy.locations import ASSETS_DIR
from entropy.misc.assets import Assets
from entropy.misc.game import Game
from entropy.misc.loader import Loader
from entropy.misc.monitor import Monitor
from entropy.misc.window import Window


__all__ = ["init", "start", "assets", "monitor", "window", "game"]

assets: Assets
monitor: Monitor
window: Window
game: Game


def init(title: str, fps: float, fonts_path: str) -> None:
    global monitor, window, game, assets

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()

    assets = Assets()
    assets.fonts.add_dir(path=ASSETS_DIR.joinpath("fonts"))
    assets.fonts.add_dir(path=fonts_path)

    monitor = Monitor()
    window = Window(
        title=title,
        fps=fps,
        dimension=(1280, 720),
        fullscreen=False,
    )

    game = Game(dimension=(1920, 1080))


def start() -> None:
    global game

    loader = Loader()
    loader.load()
    game.start()
