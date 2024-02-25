from __future__ import annotations

from abc import ABC
from enum import Enum
from enum import auto

import pygame

import entropy

from entropy.game.entity import GameEntity
from entropy.utils import Pos
from entropy.utils import Size


class ALIGN(Enum):
    CENTER = auto()
    CENTER_X = auto()
    CENTER_Y = auto()


class Component(GameEntity, ABC):
    def __init__(self):
        self._rect = pygame.Rect(0, 0, 0, 0)

    @property
    def pos(self) -> Pos:
        return Pos(*self._rect.topleft)

    @property
    def size(self) -> Size:
        return Size(*self._rect.size)

    @property
    def center(self) -> tuple[int, int]:
        return self._rect.center


class RootComponent(Component, ABC):
    def __init__(self):
        super().__init__()
        self._rect = pygame.Rect(0, 0, *entropy.window.default_res)


class UIComponent(Component, ABC):
    def __init__(self, parent: Component):
        super().__init__()
        self._parent = parent
        self.align: ALIGN | None = None

    def set_rect(self, rect: pygame.Rect) -> None:
        self._rect = rect
        self.refresh_pos()

    def refresh_pos(self):
        match self.align:
            case ALIGN.CENTER:
                self._rect.center = self._parent.center
