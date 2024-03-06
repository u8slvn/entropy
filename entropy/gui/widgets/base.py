from __future__ import annotations

from abc import ABC
from enum import StrEnum
from enum import auto

import pygame

import entropy

from entropy.event.event import Event
from entropy.game.entity import GameEntity
from entropy.utils import Pos
from entropy.utils import Size


class Align(StrEnum):
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

    @property
    def size(self) -> Size:
        return Size(*self.rect.size)

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

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
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
        align: Align | None = None,
    ):
        self.parent = parent or DefaultRoot()
        self.align = align

        rect = rect or self.parent.rect
        super().__init__(rect=rect)
        self.update_align()

    def update_align(self) -> None:
        match self.align:
            case Align.CENTER:
                self.rect.center = self.parent.center
            case Align.CENTER_X:
                self.rect.centerx = self.parent.centerx
            case Align.CENTER_Y:
                self.rect.centery = self.parent.centery
