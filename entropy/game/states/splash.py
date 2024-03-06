from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.event.types import inputs
from entropy.game.states.base import State
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import Text
from entropy.tools.timer import TimerSecond
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        font = entropy.assets.font.get("LanaPixel", "big")
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._text = Text(
            parent=self._background,
            align=Align.CENTER,
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

    def mark_as_done(self) -> None:
        self._done = True

    def setup(self) -> None:
        entropy.mixer.play_music("main-theme")
        self._text.setup()
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_event(self, event: Event) -> None:
        if event.pressed and event.key == inputs.A:
            self.mark_as_done()

    def update(self, dt: float) -> None:
        if self._done:
            self.control.transition_to("TitleScreen", with_exit=True)

        self._fade_in.update(dt=dt)
        self._fade_out.update(dt=dt)
        self._timer.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self._done:
            return

        self._background.draw(surface=surface)
        self._text.draw(surface=surface)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._done = False
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
