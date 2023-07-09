from __future__ import annotations

import pygame

from entropy.misc.game import Game
from entropy.misc.monitor import Monitor
from entropy.misc.resolution import Resolutions
from entropy.misc.window import Window
from entropy.states.menu import Menu
from entropy.states.splash import Splash


monitor: Monitor
resolutions: Resolutions
window: Window
game: Game


def init(title: str, fps: float, aspect_ratio: float) -> None:
    global monitor, window, game, resolutions

    pygame.init()

    monitor = Monitor()
    resolutions = Resolutions.build_resolutions(
        static_res=[
            ("SD", 720, 480),
            ("SHD", 1280, 720),
            ("FHD", 1920, 1080),
        ],
        monitor=monitor,
    )
    window = Window(
        title=title,
        resolution=resolutions.get("FULLSCREEN"),
        fps=fps,
        aspect_ratio=aspect_ratio,
    )
    game = Game()
    states = {
        "SPLASH": Splash(game=game),
        "MENU": Menu(game=game),
    }
    game.setup_states(states=states, default_state="SPLASH")


def start() -> None:
    global game

    game.start()
