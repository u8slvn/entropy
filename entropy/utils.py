from __future__ import annotations

from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int


class Scale(NamedTuple):
    x: float
    y: float


class Resolution(NamedTuple):
    w: int
    h: int

    @property
    def aspect_ratio(self) -> float:
        return self.w / self.h
