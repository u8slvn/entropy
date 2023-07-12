from __future__ import annotations

import pygame


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()

    @property
    def w(self):
        return self.info.current_w

    @property
    def h(self):
        return self.info.current_h

    @property
    def size(self) -> tuple[int, int]:
        return self.info.current_w, self.info.current_h
