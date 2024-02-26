from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import window
from entropy.gui.components.base import Widget
from entropy.gui.input import Inputs


if TYPE_CHECKING:
    from entropy.utils import Color


class ColorBackground(Widget):
    def __init__(self, color: Color) -> None:
        super().__init__()
        self._surf = pygame.Surface(window.default_res, pygame.SRCALPHA, 32)
        self._surf.fill(color)
        self.set_rect(self._parent.get_rect())

    def set_alpha(self, value: int) -> None:
        self._surf.set_alpha(value)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.pos)

    def teardown(self) -> None:
        pass
