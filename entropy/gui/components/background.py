from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import window
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.utils import Color


class ColorBackground(pygame.Surface):
    def __init__(self, color: Color) -> None:
        super().__init__(window.render_res, pygame.SRCALPHA, 32)
        self.fill(color)
        self.pos = Pos(0, 0)
