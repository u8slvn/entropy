from __future__ import annotations

import pygame as pg

from entropy import assets
from entropy import window


class Background:
    def __init__(self, image: pg.Surface) -> None:
        self.image = image
        self.rect = self.image.get_rect()

    def set_alpha(self, value: int) -> None:
        self.image.set_alpha(value)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)


class ImageBackground(Background):
    def __init__(self, name: str) -> None:
        super().__init__(assets.image.get(name=name))


class ColorBackground(Background):
    def __init__(self, color: pg.Color) -> None:
        super().__init__(pg.Surface(window.default_res, pg.SRCALPHA, 32))
        self.image.fill(color)
