from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.misc.action import Actions
from entropy.misc.mouse import Mouse
from entropy.states.base import State


if TYPE_CHECKING:
    from entropy.misc.control import Control


class OverlayMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        background = pg.Surface(entropy.window.render_res, pg.SRCALPHA, 32)
        background.fill((25, 15, 35, 220))
        self.background = background.convert_alpha()

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, actions: Actions, mouse: Mouse) -> None:
        if actions.SPACE:
            self.exit()

    def draw(self, surface: pg.Surface) -> None:
        self.control.prev_state.draw(surface=surface)
        surface.blit(self.background, (0, 0))
