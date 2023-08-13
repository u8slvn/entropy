from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

import pygame as pg

from entropy import mouse
from entropy.game.entity import GameEntity
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.widget import WidgetComponent
    from entropy.gui.input import Inputs


class Adjacent(IntEnum):
    NEXT = 1
    PREV = -1


class MenuWidgetGroup(GameEntity):
    def __init__(
        self,
        pos: Pos,
        margin: int,
        widgets: list[WidgetComponent],
        center_x: bool = False,
    ) -> None:
        self._focus_index: int | None = None
        self._widgets = widgets
        self._set_widgets_pos(pos=pos, margin=margin, center_x=center_x)

    def _set_widgets_pos(self, pos: Pos, margin: int, center_x: bool) -> None:
        x, y = pos

        for widget in self._widgets:
            widget.set_pos(pos=Pos(x, y), center_x=center_x)
            y += widget.get_height() + margin

    @property
    def _focused_widget(self) -> WidgetComponent | None:
        if self._focus_index is None:
            return None
        return self._widgets[self._focus_index]

    def _select_adjacent_widget(self, adjacent: Adjacent) -> None:
        if self._focus_index is None:
            self._focus_index = -1 if adjacent == Adjacent.NEXT else 0

        self._focus_index = 0 if self._focus_index is None else self._focus_index
        self._focused_widget.unset_focus()  # type: ignore
        self._focus_index = (self._focus_index + adjacent) % len(self._widgets)
        self._focused_widget.set_focus()  # type: ignore

    def setup(self) -> None:
        for button in self._widgets:
            button.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            if inputs.keyboard.UP:
                self._select_adjacent_widget(adjacent=Adjacent.PREV)
            elif inputs.keyboard.DOWN:
                self._select_adjacent_widget(adjacent=Adjacent.NEXT)

        for index, widget in enumerate(self._widgets):
            if mouse.is_visible() and widget.has_focus():
                self._focus_index = index
            widget.process_inputs(inputs=inputs)

    def update(self) -> None:
        for widget in self._widgets:
            widget.update()

    def draw(self, surface: pg.Surface) -> None:
        for widget in self._widgets:
            widget.draw(surface=surface)

    def teardown(self):
        for widget in self._widgets:
            widget.teardown()
