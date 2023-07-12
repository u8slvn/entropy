from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy.components.base import Component


if TYPE_CHECKING:
    from entropy.misc.assets import Image


class Background(Component):
    def __init__(self, image: Image) -> None:
        self.position = (0, 0)
        self.image = image

    def draw(self, display: pygame.Surface) -> None:
        display.blit(self.image.surface, self.position)
