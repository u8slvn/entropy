from __future__ import annotations

import pygame


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()

    @property
    def size(self) -> tuple[int, int]:
        return self.info.current_w, self.info.current_h
