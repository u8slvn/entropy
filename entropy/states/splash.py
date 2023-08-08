from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.commands.state import TransitionToNextState
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.states.base import State
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.gui.input import Inputs
    from entropy.misc.control import Control


class Splash(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.next_state_cmd = TransitionToNextState(
            state=self,
            next_state="TitleScreen",
        )

        self.font = entropy.assets.fonts.get("LanaPixel", "big")
        self.text = self.font.render("ENTROPY", False, "white", "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = pygame.Rect(0, 0, *entropy.window.default_res).center

        self.fade_out = FadeOut(duration=3000, callback=self.next_state_cmd)
        self.timer = TimerSecond(
            duration=2,
            autostart=False,
            callback=self.fade_out.start,
        )
        self.fade_in = FadeIn(duration=3000, callback=self.timer.start)

    def setup(self) -> None:
        self.fade_in.start()

    def process_inputs(self, inputs: Inputs) -> None:
        if any([inputs.keyboard.SPACE, inputs.keyboard.ENTER]):
            self._commands.append(self.next_state_cmd)

    def update(self, dt: float) -> None:
        self._commands()
        self.fade_in.update()
        self.fade_out.update()
        self.timer.update()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill("black")
        surface.blit(self.text, self.text_rect)
        self.fade_out.draw(surface=surface)
        self.fade_in.draw(surface=surface)

    def teardown(self) -> None:
        self.fade_out.reset()
        self.fade_in.reset()
        self.timer.reset()
