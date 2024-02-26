from __future__ import annotations

from abc import ABC
from enum import Enum
from enum import auto

import pygame

import entropy

from entropy.game.entity import GameEntity
from entropy.gui.input import Inputs
from entropy.utils import Pos
from entropy.utils import Size


class ALIGN(Enum):
    CENTER = auto()
    CENTER_X = auto()
    CENTER_Y = auto()


class BaseWidget(GameEntity, ABC):
    _default_rect = pygame.Rect(0, 0, 0, 0)

    def __init__(self) -> None:
        self._rect = self._default_rect

    def get_rect(self) -> pygame.Rect:
        return self._rect

    @property
    def pos(self) -> Pos:
        return Pos(*self._rect.topleft)

    @property
    def size(self) -> Size:
        return Size(*self._rect.size)

    @property
    def center(self) -> tuple[int, int]:
        return self._rect.center

    @property
    def centery(self) -> int:
        return self._rect.centery

    @property
    def centerx(self) -> int:
        return self._rect.centerx

    def set_focus(self) -> None:
        pass

    def unset_focus(self) -> None:
        pass

    def has_focus(self) -> None:
        pass


class DefaultRoot(BaseWidget):
    _default_rect = pygame.Rect(0, 0, *entropy.window.default_res)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass


class Widget(BaseWidget, ABC):
    def __init__(self, parent: Widget | None = None) -> None:
        super().__init__()
        self._parent = parent or DefaultRoot()
        self.align: ALIGN | None = None

    def set_rect(self, rect: pygame.Rect) -> None:
        self._rect = rect
        self.refresh_pos()

    def refresh_pos(self) -> None:
        match self.align:
            case ALIGN.CENTER:
                self._rect.center = self._parent.center
            case ALIGN.CENTER_X:
                self._rect.centerx = self._parent.centerx
            case ALIGN.CENTER_Y:
                self._rect.centery = self._parent.centery
