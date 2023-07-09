from __future__ import annotations

import pygame

from entropy.misc.game import Game
from entropy.misc.monitor import Monitor
from entropy.misc.window import Window


__all__ = ["init", "start", "monitor", "window", "game"]


monitor: Monitor
window: Window
game: Game


def init(title: str, fps: float, aspect_ratio: float) -> None:
    global monitor, window, game

    pygame.init()

    # _Y_OFFSET = (pygame.display.Info().current_w - SCREEN_SIZE[0]) // 2
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(_Y_OFFSET, 25)

    monitor = Monitor()
    window = Window(
        title=title,
        fps=fps,
        aspect_ratio=aspect_ratio,
        dimension=(1280, 720),
        fullscreen=False,
    )
    game = Game()


def start() -> None:
    global game

    game.start()
