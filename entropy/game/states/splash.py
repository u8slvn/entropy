from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.game.states.base import State
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.base import ALIGN
from entropy.gui.components.text import Text
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.tools.timer import TimerSecond
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        font = entropy.assets.fonts.get("LanaPixel", "big")
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._text = Text(
            parent=self._background,
            align=ALIGN.CENTER,
            font=font,
            text="ENTROPY",
            color="white",
        )
        self._fade_out = FadeOut(duration=4000, callback=self.mark_as_done)
        self._timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=4000, callback=self._timer.start)
        self._done = False

    def mark_as_done(self):
        self._done = True

    def setup(self) -> None:
        entropy.mixer.play_music("main-theme")
        self._text.setup()
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

        self._background.draw(surface=surface)
        self._text.draw(surface=surface)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        self._done = False
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
