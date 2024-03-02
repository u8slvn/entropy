from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.game.states.base import State
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.base import ALIGN
from entropy.gui.widgets.text import TypeWriterText
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


class Play(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        font = entropy.assets.fonts.get("LanaPixel", "big")
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._text = TypeWriterText(
            parent=self._background,
            font=font,
            text="Gamer Barbany était un prodige des mondes virtuels, où il régnait en maître. Mais son plus grand défi l'attendait dans la réalité, où il trouva l'amour, dépassant ainsi les limites de son écran pour découvrir un univers bien plus vaste et profond.",
            color="white",
            width=600,
            speed=1.4,
            align=ALIGN.CENTER,
        )

    def setup(self) -> None:
        self._text.setup()

    def process_inputs(self, inputs: Inputs) -> None: ...

    def update(self) -> None:
        self._text.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)
        self._text.draw(surface=surface)

    def teardown(self) -> None: ...
