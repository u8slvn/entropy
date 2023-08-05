from __future__ import annotations

from typing import NamedTuple

import pygame


class Pos(NamedTuple):
    """2D coordinate position."""

    x: int
    y: int


class Scale(NamedTuple):
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

    @property
    def aspect_ratio(self) -> float:
        return self.w / self.h


class Color(pygame.Color):
    """Color object."""

    pass
