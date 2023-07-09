from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.event

from entropy.colors import BLACK, WHITE
from entropy.states import State


if TYPE_CHECKING:
    import pygame

    from entropy import Game


class Menu(State):
    def __init__(self, game: Game):
        super().__init__(game=game)
        self.font = pygame.font.SysFont("Verdana", 16)
        self.text = self.font.render("THIS IS THE MENU", True, BLACK)

    def setup(self) -> None:
        pass

    def process_event(self, event: pygame.event.Event) -> None:
        ...

    def update(self) -> None:
        pass

    def render(self, display: pygame.Surface) -> None:
        display.fill(WHITE)
        pos_x = (display.get_width() - self.text.get_width()) / 2
        pos_y = (display.get_height() - self.text.get_height()) / 2
        display.blit(self.text, (pos_x, pos_y))

    def teardown(self) -> None:
        pass
