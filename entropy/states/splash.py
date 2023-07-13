from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.event

import entropy
from entropy.colors import BLACK, WHITE
from entropy.states import State


if TYPE_CHECKING:
    import pygame as pg


class Splash(State):
    def __init__(self):
        super().__init__()
        self.countdown = 10
        self.countdown_event = pygame.USEREVENT + 1
        self.alpha = 0
        self.alpha_rate = 1
        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", True, WHITE, BLACK)
        self.text.set_alpha(self.alpha)
        pygame.time.set_timer(self.countdown_event, 1000)

    def handle_event(self, event: pg.event.Event, mouse_pos: tuple[int, int]) -> None:
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

    def draw(self, surface) -> None:
        surface.fill(BLACK)
        x = (surface.get_width() - self.text.get_width()) // 2
        y = (surface.get_height() - self.text.get_height()) // 2
        surface.blit(self.text, (x, y))

    def cleanup(self) -> None:
        super().cleanup()
        self.alpha = 0
        self.countdown = 10
