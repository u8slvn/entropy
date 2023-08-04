from __future__ import annotations

from typing import NamedTuple

import pygame


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


class Timer:
    def __init__(self, countdown: int) -> None:
        self._default_countdown = countdown
        self._countdown = self._default_countdown
        self._start_ticks = 0
        self._stopped = False

    @property
    def countdown(self) -> int:
        return self._countdown

    def start(self) -> None:
        self._countdown = self._default_countdown
        self._start_ticks = pygame.time.get_ticks()

    def stop(self) -> None:
        self._stopped = False

    def is_finished(self) -> bool:
        return self._countdown <= 0

    def update(self) -> None:
        if self._stopped is True:
            return

        ticks = pygame.time.get_ticks() - self._start_ticks
        self._countdown = self._default_countdown - ticks
        if self._countdown <= 0:
            self.stop()


class TimerSecond(Timer):
    def __init__(self, countdown: int) -> None:
        super().__init__(countdown=countdown * 1000)

    @property
    def countdown(self):
        return self._countdown // 1000
