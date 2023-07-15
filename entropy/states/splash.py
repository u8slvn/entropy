from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.states import State
from entropy.states.title_screen import TitleScreen


if TYPE_CHECKING:
    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.countdown = 10
        self.countdown_event = pg.USEREVENT + 1
        self.alpha = 0
        self.alpha_rate = 1
        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", False, "white", "black")
        self.text.set_alpha(self.alpha)
        pg.time.set_timer(self.countdown_event, 1000)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == self.countdown_event:
            self.countdown -= 1

    def update(self, actions: Actions, mouse: Mouse) -> None:
        if any([actions.SPACE, actions.ENTER]) or self.countdown == 0:
            self.control.transition_to(state=TitleScreen)
            self.cleanup()

        if self.countdown < 5:
            self.alpha = max(self.alpha - self.alpha_rate, 0)
        else:
            self.alpha = min(self.alpha + self.alpha_rate, 255)
        self.text.set_alpha(self.alpha)

    def draw(self, surface) -> None:
        surface.fill("black")
        x = (surface.get_width() - self.text.get_width()) // 2
        y = (surface.get_height() - self.text.get_height()) // 2
        surface.blit(self.text, (x, y))

    def cleanup(self) -> None:
        self.countdown = 10
        self.alpha = 0
