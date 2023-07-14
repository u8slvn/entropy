from __future__ import annotations

import pygame as pg

from entropy.misc.mouse import Mouse
from entropy.utils import Pos


class Button(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, image_hover: pg.Surface, pos: Pos) -> None:
        super().__init__()
        self.hover = False
        self.images = [image, image_hover]
        self.image = self.images[self.hover]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, mouse: Mouse) -> None:
        self.hover = self.rect.collidepoint(mouse.pos)
        self.image = self.images[self.hover]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)
