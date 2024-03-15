from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Literal

from entropy.event.specs import down_is_pressed
from entropy.event.specs import left_is_pressed
from entropy.event.specs import right_is_pressed
from entropy.event.specs import up_is_pressed


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.gui.component.base import Sprite


class Adjacent(IntEnum):
    NEXT = 1
    PREV = -1


class Menu:
    def __init__(
        self,
        items: list[Sprite],
        direction: Literal["vertical", "horizontal"],
    ) -> None:
        self.focus_index: int | None = None
        self.items = items
        self.direction = direction

    @property
    def _focused_sprite(self) -> Sprite | None:
        if self.focus_index is None:
            return None
        return self.items[self.focus_index]

    def _select_adjacent_sprite(self, adjacent: Adjacent) -> None:
        if self.focus_index is None:
            self.focus_index = -1 if adjacent == Adjacent.NEXT else 0

        self.focus_index = 0 if self.focus_index is None else self.focus_index
        self._focused_sprite.unset_focus()  # type: ignore
        self.focus_index = (self.focus_index + adjacent) % len(self.items)
        self._focused_sprite.set_focus()  # type: ignore

    def process_event(self, event: Event) -> None:
        if self.direction == "vertical":
            if up_is_pressed(event):
                self._select_adjacent_sprite(adjacent=Adjacent.PREV)
            elif down_is_pressed(event):
                self._select_adjacent_sprite(adjacent=Adjacent.NEXT)
        else:
            if left_is_pressed(event):
                self._select_adjacent_sprite(adjacent=Adjacent.PREV)
            elif right_is_pressed(event):
                self._select_adjacent_sprite(adjacent=Adjacent.NEXT)
