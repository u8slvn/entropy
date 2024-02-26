from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import assets
from entropy import window
from entropy.gui.components.base import Widget
from entropy.gui.input import Inputs


if TYPE_CHECKING:
    from entropy.utils import Color


class ImageBackground(Widget):
    def __init__(self, name: str) -> None:
        self.surf = assets.images.get(name=name)
        super().__init__(rect=self.surf.get_rect())

    def set_alpha(self, value: int) -> None:
        self.surf.set_alpha(value)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, self.pos)

    def teardown(self) -> None:
        pass


class ColorBackground(Widget):
    def __init__(self, color: Color) -> None:
        self.surf = pygame.Surface(window.default_res, pygame.SRCALPHA, 32)
        self.surf.fill(color)
        super().__init__(rect=self.surf.get_rect())

    def set_alpha(self, value: int) -> None:
        self.surf.set_alpha(value)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, self.pos)

    def teardown(self) -> None:
        pass
