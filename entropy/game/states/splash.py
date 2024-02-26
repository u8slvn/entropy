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
        self.background = ColorBackground(color=Color(0, 0, 0, 255))
        self.text = Text(
            parent=self.background,
            align=ALIGN.CENTER,
            font=font,
            text="ENTROPY",
            color="white",
        )
        self.fade_out = FadeOut(duration=4000, callback=self.mark_as_done)
        self.timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self.fade_out.activate,
        )
        self.fade_in = FadeIn(duration=4000, callback=self.timer.start)
        self.done = False

    def mark_as_done(self):
        self.done = True

    def setup(self) -> None:
        entropy.mixer.play_music("main-theme")
        self.text.setup()
        self.fade_in.setup()
        self.fade_out.setup()
        self.timer.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE or inputs.keyboard.ENTER:
            self.mark_as_done()

    def update(self) -> None:
        if self.done:
            self.control.transition_to("TitleScreen")

        self.fade_in.update()
        self.fade_out.update()
        self.timer.update()

    def draw(self, surface: pygame.Surface) -> None:
        if self.done:
            return

        self.background.draw(surface=surface)
        self.text.draw(surface=surface)
        self.fade_out.draw(surface=surface)
        self.fade_in.draw(surface=surface)

    def teardown(self) -> None:
        self.done = False
        self.fade_out.teardown()
        self.fade_in.teardown()
        self.timer.teardown()
