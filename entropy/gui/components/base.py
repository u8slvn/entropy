from __future__ import annotations

from abc import ABC
from enum import Enum
from enum import auto

import entropy

from entropy.game.entity import GameEntity
from entropy.utils import Pos
from entropy.utils import Size


class ALIGN(Enum):
    CENTER = auto()
    CENTER_X = auto()
    CENTER_Y = auto()


class Component(GameEntity, ABC):
    def __init__(
        self,
        parent: Component | None,
    ):
        self._parent = parent
        self.size = Size(0, 0)
        self.pos = Pos(0, 0)
        self.align: ALIGN | None = None

    def set_size(self, w: int, h: int) -> None:
        self.size = Size(w, h)

    def set_pos(self, pos: Pos, align: ALIGN | None = None) -> None:
        self.pos = pos
        self.align = align
        self.refresh_pos()

    def refresh_pos(self):
        match self.align:
            case ALIGN.CENTER:
                x = (self._parent.size.w - self.size.w) // 2
                y = (self._parent.size.h - self.size.h) // 2
                self.pos = Pos(x, y)


class RootComponent(Component, ABC):
    def __init__(self):
        super().__init__(parent=None)
        self.set_pos(pos=Pos(0, 0))
        self.set_size(*entropy.window.default_res)
