from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from entropy.gui.components.background import ColorBackground
from entropy.states.base import State
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents
    from entropy.misc.control import Control


class OverlayMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.background = ColorBackground(color=Color(25, 15, 35, 220))

    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        if keyboard_e.SPACE:
            self.exit()

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface=surface)
        surface.blit(self.background, self.background.pos)
