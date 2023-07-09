from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.event

import entropy
from entropy.colors import BLACK, WHITE
from entropy.states import State


if TYPE_CHECKING:
    import pygame

    from entropy import Game


class Splash(State):
    def __init__(self, game: Game):
        super().__init__(game=game)
        self.countdown = 10
        self.countdown_event = pygame.USEREVENT + 1

        self.alpha = 0
        self.alpha_rate = 1
        self.font = entropy.assets.fonts.get("LanaPixel", 100)
        self.text = self.font.render("ENTROPY", True, WHITE, BLACK)
        self.text.set_alpha(self.alpha)

        pygame.time.set_timer(self.countdown_event, 1000)

    def setup(self) -> None:
        ...

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYUP or self.countdown == 0:
            self.game.transition_to("MENU")
        elif event.type == self.countdown_event:
            self.countdown -= 1

    def update(self) -> None:
        if self.countdown < 5:
            self.alpha = max(self.alpha - self.alpha_rate, 0)
        else:
            self.alpha = min(self.alpha + self.alpha_rate, 255)
        self.text.set_alpha(self.alpha)

    def render(self, display) -> None:
        display.fill(BLACK)
        pos_x = (display.get_width() - self.text.get_width()) / 2
        pos_y = (display.get_height() - self.text.get_height()) / 2
        display.blit(self.text, (pos_x, pos_y))

    def teardown(self) -> None:
        self.alpha = 0
        self.countdown = 10
