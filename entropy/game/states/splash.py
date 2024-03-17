from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.event.specs import a_is_pressed
from entropy.game.states.base import State
from entropy.gui.elements.background import ColorBackground
from entropy.gui.elements.text import Text
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.background = ColorBackground(pg.Color("black"))
        self.text = Text(
            None,
            font=entropy.assets.font.get("LanaPixel", "md"),
            text="ENTROPY",
            color=pg.Color("white"),
            translate=False,
            center=self.background.rect.center,
        )
        self.fade_out = FadeOut(duration=4000, callback=self.mark_as_done)
        self.timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self.fade_out.activate,
        )
        self.fade_in = FadeIn(duration=4000, callback=self.timer.start)
        self._done = False

    def mark_as_done(self) -> None:
        self._done = True

    def setup(self) -> None:
        entropy.mixer.play_music("main-theme")
        self.fade_in.setup()
        self.fade_out.setup()
        self.timer.setup()

    def process_event(self, event: Event) -> None:
        if a_is_pressed(event):
            self.mark_as_done()

    def update(self, dt: float) -> None:
        if self._done:
            self.control.transition_to("TitleScreen", with_exit=True)

        self.fade_in.update(dt)
        self.fade_out.update(dt)
        self.timer.update(dt)

    def draw(self, surface: pg.Surface) -> None:
        if self._done:
            return

        self.background.draw(surface)
        self.text.draw(surface)
        self.fade_out.draw(surface)
        self.fade_in.draw(surface)

    def teardown(self) -> None:
        super().teardown()
        self._done = False
        self.fade_out.teardown()
        self.fade_in.teardown()
        self.timer.teardown()
