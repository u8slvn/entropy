from __future__ import annotations

import pygame

import entropy
from entropy.colors import WHITE
from entropy.locations import ASSETS_DIR


class Loader:
    dimension = (492, 72)

    def __init__(self) -> None:
        self.display = pygame.Surface(self.dimension)
        self.loading = False
        self.counter = 1000
        self.total = 1000
        self.bar = pygame.image.load(
            ASSETS_DIR.joinpath("loader/bar.png")
        ).convert_alpha()
        self.max_progress = 476
        self.progress = pygame.Surface((2, 54))
        self.progress.fill(WHITE)
        self.done_count = 0

    def update(self):
        self.counter -= 3
        self.loading = self.counter > 0
        done = self.total - self.counter
        percent_done = done * 100 / self.total
        self.done_count = round((percent_done * self.max_progress) / 100)

    def render(self):
        self.display.blit(self.bar, (0, 0))
        self.display.blit(
            pygame.transform.scale(self.progress, (self.done_count, 54)), (8, 8)
        )
        entropy.window.draw(display=self.display, keep_ratio=False)

    def load(self) -> None:
        self.loading = True

        while self.loading:
            _ = pygame.event.get()
            self.update()
            self.render()
