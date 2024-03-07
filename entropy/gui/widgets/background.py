from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import assets
from entropy import window
from entropy.event.event import Event
from entropy.gui.widgets.base import Widget


if TYPE_CHECKING:
    from entropy.utils.measure import Color


class Background(Widget):
    def __init__(self, surf: pygame.Surface) -> None:
        self._surf = surf
        super().__init__(rect=self._surf.get_rect())

    def set_alpha(self, value: int) -> None:
        self._surf.set_alpha(value)

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect)

    def teardown(self) -> None:
        pass


class ImageBackground(Background):
    def __init__(self, name: str) -> None:
        surf = assets.image.get(name=name)
        super().__init__(surf=surf)


class ColorBackground(Background):
    def __init__(self, color: Color) -> None:
        surf = pygame.Surface(window.default_res, pygame.SRCALPHA, 32)
        surf.fill(color)
        super().__init__(surf=surf)
