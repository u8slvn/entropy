from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

import pygame as pg

from entropy import mouse


if TYPE_CHECKING:
    from entropy.gui.components.button import Button
    from entropy.gui.input import Inputs


class Adjacent(IntEnum):
    NEXT = 1
    PREV = -1


class MenuButtonGroup:
    def __init__(self, buttons: list[Button]) -> None:
        self._focus_index: int | None = None
        self._buttons = buttons

    def _select_adjacent_button(self, adjacent: Adjacent) -> None:
        if self._focus_index is None:
            self._focus_index = -1 if adjacent == Adjacent.NEXT else 0

        self._focus_index = 0 if self._focus_index is None else self._focus_index
        self._focused_button.unset_focus()
        self._focus_index = (self._focus_index + adjacent) % len(self._buttons)
        self._focused_button.set_focus()

    @property
    def _focused_button(self) -> Button | None:
        if self._focus_index is None:
            return None
        return self._buttons[self._focus_index]

    def process_inputs(self, inputs: Inputs, dt: float) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            if inputs.keyboard.UP:
                self._select_adjacent_button(adjacent=Adjacent.PREV)
            elif inputs.keyboard.DOWN:
                self._select_adjacent_button(adjacent=Adjacent.NEXT)
            elif inputs.keyboard.ENTER:
                if self._focused_button is not None:
                    self._focused_button.press()

        for index, button in enumerate(self._buttons):
            if mouse.is_visible() and button.has_focus():
                self._focus_index = index
            button.process_inputs(inputs=inputs, dt=dt)

    def update(self) -> None:
        for button in self._buttons:
            button.update()

    def draw(self, surface: pg.Surface) -> None:
        for button in self._buttons:
            button.draw(surface=surface)
