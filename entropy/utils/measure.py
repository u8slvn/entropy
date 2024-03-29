from __future__ import annotations

import gc

from typing import Any
from typing import NamedTuple

import pygame


def _is_2d_vector(value: tuple[int, int]) -> bool:
    return len(value) == 2 and all(isinstance(e, int) for e in value)


class Pos(NamedTuple):
    """2D coordinate position."""

    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> Pos:  # type: ignore[override]
        assert _is_2d_vector(other)
        return Pos(self.x + other[0], self.y + other[1])

    def __sub__(self, other: tuple[int, int]) -> Pos:
        assert _is_2d_vector(other)
        return Pos(self.x - other[0], self.y - other[1])


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

    @property
    def aspect_ratio(self) -> float:
        return self.w / self.h

    def __add__(self, other: tuple[int, int]) -> Res:  # type: ignore[override]
        assert _is_2d_vector(other)
        return Res(self.w + other[0], self.h + other[1])

    def __sub__(self, other: tuple[int, int]) -> Res:
        assert _is_2d_vector(other)
        return Res(self.w - other[0], self.h - other[1])

    def __str__(self) -> str:
        return f"{self.w}x{self.h}"


class Color(pygame.Color):
    """Color object."""

    pass


def cleanup(obj: Any) -> None:
    del obj
    gc.collect()
