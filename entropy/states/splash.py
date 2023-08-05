from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.states.base import State
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)

        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", False, "white", "black")

        self.transition_out = FadeOut(
            size=entropy.window.render_res,
            duration=3000,
            callback=self.next_state,
        )
        self.timer = TimerSecond(
            duration=4,
            autostart=False,
            callback=self.transition_out.start,
        )
        self.transition_in = FadeIn(
            size=entropy.window.render_res,
            duration=3000,
            callback=self.timer.start,
        )

    def handle_event(self, event: pg.event.Event) -> None:
        ...

    def update(self, actions: Actions, mouse: Mouse) -> None:
        self.transition_in.update()
        self.transition_out.update()
        self.timer.update()

        if any([actions.SPACE, actions.ENTER]):
            self.next_state()

    def draw(self, surface) -> None:
        surface.fill("black")
        x = (surface.get_width() - self.text.get_width()) // 2
        y = (surface.get_height() - self.text.get_height()) // 2
        surface.blit(self.text, (x, y))
        self.transition_out.draw(surface=surface)
        self.transition_in.draw(surface=surface)

    def next_state(self) -> None:
        self.transition_out.reset()
        self.transition_in.reset()
        self.timer.reset()
        self.control.transition_to(state="TitleScreen")
