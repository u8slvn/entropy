from __future__ import annotations

import pygame

from entropy.utils import Res


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()

    @property
    def res(self) -> Res:
        return Res(self.info.current_w, self.info.current_h)
