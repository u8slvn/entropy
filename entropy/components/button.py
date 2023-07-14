from __future__ import annotations

import pygame as pg

from entropy.misc.mouse import Mouse
from entropy.utils import Pos


class Button(pg.sprite.Sprite):
    def __init__(
        self,
        image: pg.Surface,
        image_hover: pg.Surface,
        sound_hover: pg.mixer.Sound,
        pos: Pos,
    ) -> None:
        super().__init__()
        self.hover = False
        self.images = [image, image_hover]
        self.image = self.images[self.hover]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.sound_hover = sound_hover

    def update(self, mouse: Mouse) -> None:
        hover = self.rect.collidepoint(mouse.pos)
        if hover is True and self.hover is False:
            self.sound_hover.play()
        self.hover = hover
        self.image = self.images[self.hover]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)
