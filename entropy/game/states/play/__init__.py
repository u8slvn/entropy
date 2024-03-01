from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy.game.states.base import State


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


class Play(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)

    def setup(self) -> None: ...

    def process_inputs(self, inputs: Inputs) -> None: ...

    def update(self) -> None: ...

    def draw(self, surface: pygame.Surface) -> None: ...

    def teardown(self) -> None: ...
