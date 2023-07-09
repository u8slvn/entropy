from __future__ import annotations

import pygame

import entropy
from entropy.locations import ASSETS_DIR


class Loader:
    def __init__(self) -> None:
        self.display = pygame.Surface((1920, 1080))
        self.loading = False
        self.logo = pygame.image.load(
            ASSETS_DIR.joinpath("loader/logo.png")
        ).convert_alpha()
        self.counter = 1000

    def update(self):
        self.counter -= 3
        self.loading = self.counter > 0

    def render(self):
        self.display.blit(self.logo, (100, 100))
        entropy.window.draw(self.display)

    def load(self) -> None:
        self.loading = True

        while self.loading:
            _ = pygame.event.get()
            self.update()
            self.render()
