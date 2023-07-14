from __future__ import annotations

from typing import TYPE_CHECKING

import entropy
from entropy.states import State


if TYPE_CHECKING:
    import pygame as pg


class Menu(State):
    position = (0, 100)

    def __init__(self):
        super().__init__()
        self.background = entropy.assets.images.get("menu-bg")

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
