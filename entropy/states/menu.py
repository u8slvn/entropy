from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy
from entropy.states import State


if TYPE_CHECKING:
    from entropy.misc.game import Game


class Menu(State):
    position = (0, 100)

    def __init__(self, game: Game):
        super().__init__(game=game)
        self.background = entropy.assets.images.get("menu-bg")

    def setup(self) -> None:
        ...

    def process_event(self, event: pygame.event.Event) -> None:
        ...

    def update(self) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.background, (0, 0))

    def teardown(self) -> None:
        pass
