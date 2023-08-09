from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.game.states.base import State
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        font = entropy.assets.fonts.get("LanaPixel", "big")
        self._text = font.render("ENTROPY", False, "white", "black")
        self._text_rect = self._text.get_rect()
        self._text_rect.center = pygame.Rect(0, 0, *entropy.window.default_res).center
        self._fade_out = FadeOut(duration=3000, callback=self.mark_as_done)
        self._timer = TimerSecond(
            duration=2,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=3000, callback=self._timer.start)
        self._done = False

    def mark_as_done(self):
        self._done = True

    def setup(self) -> None:
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE or inputs.keyboard.ENTER:
            self.mark_as_done()

    def update(self) -> None:
        if self._done:
            self.control.transition_to("TitleScreen")

        self._fade_in.update()
        self._fade_out.update()
        self._timer.update()

    def draw(self, surface: pygame.Surface) -> None:
        if self._done:
            return

        surface.fill("black")
        surface.blit(self._text, self._text_rect)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        self._done = False
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
