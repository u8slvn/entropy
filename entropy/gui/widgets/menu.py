from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

import pygame

from entropy import mouse
from entropy.gui.widgets.base import Widget


if TYPE_CHECKING:
    from entropy.gui.input import Inputs


class Adjacent(IntEnum):
    NEXT = 1
    PREV = -1


class Group(Widget):
    def __init__(
        self,
        parent: Widget,
    ) -> None:
        self.widgets = []
        super().__init__(parent=parent)

    def add_widget(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def add_widgets(self, widgets: list[Widget]) -> None:
        self.widgets.extend(widgets)

    def setup(self) -> None:
        for widget in self.widgets:
            widget.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        for widget in self.widgets:
            widget.process_inputs(inputs=inputs)

    def update(self) -> None:
        for widget in self.widgets:
            widget.update()

    def draw(self, surface: pygame.Surface) -> None:
        for widget in self.widgets:
            widget.draw(surface=surface)

    def teardown(self):
        for widget in self.widgets:
            widget.teardown()


class MenuGroup(Group):
    def __init__(
        self,
        parent: Widget,
    ) -> None:
        self.focus_index: int | None = None
        super().__init__(parent=parent)

    @property
    def _focused_widget(self) -> Widget | None:
        if self.focus_index is None:
            return None
        return self.widgets[self.focus_index]

    def _select_adjacent_widget(self, adjacent: Adjacent) -> None:
        if self.focus_index is None:
            self.focus_index = -1 if adjacent == Adjacent.NEXT else 0

        self.focus_index = 0 if self.focus_index is None else self.focus_index
        self._focused_widget.unset_focus()  # type: ignore
        self.focus_index = (self.focus_index + adjacent) % len(self.widgets)
        self._focused_widget.set_focus()  # type: ignore

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            if inputs.keyboard.UP:
                self._select_adjacent_widget(adjacent=Adjacent.PREV)
            elif inputs.keyboard.DOWN:
                self._select_adjacent_widget(adjacent=Adjacent.NEXT)

        for index, widget in enumerate(self.widgets):
            if mouse.is_visible() and widget.has_focus():
                self.focus_index = index
            widget.process_inputs(inputs=inputs)