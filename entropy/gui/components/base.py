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
    def __init__(self, rect: pygame.Rect) -> None:
        self._rect = rect

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @rect.setter
    def rect(self, rect: pygame.Rect) -> None:
        self._rect = rect

    @property
    def pos(self) -> Pos:
        return Pos(*self.rect.topleft)

    @pos.setter
    def pos(self, pos: Pos) -> None:
        self.rect.topleft = pos

    @property
    def size(self) -> Size:
        return Size(*self.rect.size)

    @size.setter
    def size(self, size: Size) -> None:
        self.rect.size = size

    @property
    def center(self) -> tuple[int, int]:
        return self.rect.center

    @property
    def centery(self) -> int:
        return self.rect.centery

    @property
    def centerx(self) -> int:
        return self.rect.centerx

    def set_focus(self) -> None:
        pass

    def unset_focus(self) -> None:
        pass

    def has_focus(self) -> None:
        pass


class DefaultRoot(BaseWidget):
    def __init__(self) -> None:
        super().__init__(rect=pygame.Rect(0, 0, *entropy.window.default_res))

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
    def __init__(
        self,
        parent: Widget | None = None,
        rect: pygame.Rect | None = None,
        align: ALIGN | None = None,
    ):
        self.parent = parent or DefaultRoot()
        self.align = align

        super().__init__(rect=rect)
        self.update_align()

    def update_align(self) -> None:
        match self.align:
            case ALIGN.CENTER:
                self.rect.center = self.parent.center
            case ALIGN.CENTER_X:
                self.rect.centerx = self.parent.centerx
            case ALIGN.CENTER_Y:
                self.rect.centery = self.parent.centery
