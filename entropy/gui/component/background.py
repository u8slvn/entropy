from __future__ import annotations

import pygame as pg

from entropy import window


class Background(pg.Surface):
    rect = window.screen_rect

    def __init__(self):
        super().__init__(self.rect.size, pg.SRCALPHA, 32)


class ColorBackground(Background):
    def __init__(self, color: pg.Color) -> None:
        super().__init__()
        self.fill(color)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self, self.rect)
