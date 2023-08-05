from __future__ import annotations

from typing import TYPE_CHECKING

import entropy

from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.states.base import State
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents
    from entropy.misc.control import Control


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)

        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", False, "white", "black")

        self.fade_out = FadeOut(duration=3000, callback=self.next_state)
        self.timer = TimerSecond(
            duration=4,
            autostart=False,
            callback=self.fade_out.start,
        )
        self.fade_in = FadeIn(duration=3000, callback=self.timer.start)

    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        self.fade_in.update()
        self.fade_out.update()
        self.timer.update()

        if any([keyboard_e.SPACE, keyboard_e.ENTER]):
            self.next_state()

    def draw(self, surface) -> None:
        surface.fill("black")
        x = (surface.get_width() - self.text.get_width()) // 2
        y = (surface.get_height() - self.text.get_height()) // 2
        surface.blit(self.text, (x, y))
        self.fade_out.draw(surface=surface)
        self.fade_in.draw(surface=surface)

    def next_state(self) -> None:
        self.fade_out.reset()
        self.fade_in.reset()
        self.timer.reset()
        self.control.transition_to(state="TitleScreen")
