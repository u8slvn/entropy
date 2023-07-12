from __future__ import annotations

from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from entropy import Game
    from entropy.misc.assets import Image


class Scaler:
    def __init__(self, game: Game):
        self.game = game

    def get_scale_percent(self, value: tuple[int, int]) -> tuple[float, float]:
        return (
            value[0] / self.game.max_resolution.width,
            value[1] / self.game.max_resolution.height,
        )

    def scale(self, image: Image) -> None:
        if (
            self.game.fullscreen
            or self.game.screen_resolution == self.game.max_resolution
        ):
            image.surface = image.original
        else:
            w = image.scale_percent_w * self.game.screen_resolution.width
            h = image.scale_percent_h * self.game.screen_resolution.height
            image.surface = pygame.transform.scale(image.original, (w, h))
