from __future__ import annotations

from typing import NamedTuple

import pygame


class Pos(NamedTuple):
    """2D coordinate position."""

    x: int
    y: int

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Pos) -> Pos:
        return Pos(self.x - other.x, self.y - other.y)


class PosScale(NamedTuple):
    """2D scale."""

    x: float
    y: float


class Size(NamedTuple):
    """2D dimension."""

    w: int
    h: int


class Res(NamedTuple):
    """Screen resolution."""

    w: int
    h: int

    def __add__(self, other: Res) -> Res:
        return Res(self.w + other.w, self.h + other.h)

    def __sub__(self, other: Res) -> Res:
        return Res(self.w - other.w, self.h - other.h)

    @property
    def size(self) -> tuple[int, int]:
        return self.w, self.h

    @property
    def aspect_ratio(self) -> float:
        return self.w / self.h

    def __str__(self) -> str:
        return f"{self.w}x{self.h}"


class Color(pygame.Color):
    """Color object."""

    pass
