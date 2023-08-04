from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.gui.transistions.fader import FadeIn
from entropy.states.base import State
from entropy.utils import TimerSecond


if TYPE_CHECKING:
    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.timer = TimerSecond(countdown=10)
        self.timer.start()
        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", False, "white", "black")
        self.text_rect = self.text.get_rect()
        self.transition_in = FadeIn(entropy.window.render_res, duration=3000)

    def handle_event(self, event: pg.event.Event) -> None:
        ...

    def update(self, actions: Actions, mouse: Mouse) -> None:
        self.transition_in.update()
        self.timer.update()
        if any([actions.SPACE, actions.ENTER]) or self.timer.is_finished():
            self.control.transition_to(state="TitleScreen")

    def draw(self, surface) -> None:
        surface.fill("black")
        x = (surface.get_width() - self.text.get_width()) // 2
        y = (surface.get_height() - self.text.get_height()) // 2
        surface.blit(self.text, (x, y))
        self.transition_in.draw(surface=surface)
