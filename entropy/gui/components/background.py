from __future__ import annotations

from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from entropy.utils import Color
    from entropy.utils import Size


class ColorBackground(pygame.Surface):
    def __init__(self, size: Size, color: Color) -> None:
        super().__init__(size, pygame.SRCALPHA, 32)
        self.fill(color)
