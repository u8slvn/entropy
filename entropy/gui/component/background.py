from __future__ import annotations

import pygame as pg

from entropy import window


class Background(pg.Surface):
    def __init__(self) -> None:
        super().__init__(window.default_res, pg.SRCALPHA, 32)
        self.rect = self.get_rect()


class ColorBackground(Background):
    def __init__(self, color: pg.Color) -> None:
        super().__init__()
        self.fill(color)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self, self.rect)
