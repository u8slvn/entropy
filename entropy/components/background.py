from __future__ import annotations

import pygame

import entropy
from entropy.components import Component


class Background(Component):
    def __init__(self, image_name: str) -> None:
        self.position = (0, 0)
        self.image = entropy.assets.images.get(name=image_name)

    def draw(self, display: pygame.Surface) -> None:
        display.blit(self.image, self.position)
