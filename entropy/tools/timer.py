from __future__ import annotations

from typing import Callable

import pygame


class Timer:
    def __init__(
        self,
        duration: int,
        autostart: bool = True,
        callback: Callable[[], None] | None = None,
    ) -> None:
        self._duration = duration
        self._countdown = self._duration
        self._autostart = autostart
        self._callback = callback
        self._start_ticks = 0
        self._started = False
        self._done = False

        if self._autostart is True:
            self.start()

    def _trigger_callback(self) -> None:
        if self._callback is not None:
            self._callback()

    @property
    def countdown(self) -> int:
        return self._countdown

    def start(self) -> None:
        if self.is_started():
            return

        self._started = True
        self._start_ticks = pygame.time.get_ticks()

    def stop(self) -> None:
        self._start_ticks = 0
        self._done = True

    def is_started(self) -> bool:
        return self._started

    def is_done(self) -> bool:
        return self._done

    def update(self) -> None:
        if self.is_done() or not self.is_started():
            return

        ticks = pygame.time.get_ticks() - self._start_ticks
        self._countdown = self._duration - ticks
        if self._countdown <= 0:
            self._trigger_callback()
            self.stop()

    def reset(self) -> None:
        self._countdown = self._duration
        self._start_ticks = 0
        self._started = False
        self._done = False

        if self._autostart is True:
            self.start()


class TimerSecond(Timer):
    def __init__(
        self,
        duration: int,
        autostart: bool = True,
        callback: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            duration=duration * 1000, callback=callback, autostart=autostart
        )

    @property
    def countdown(self):
        return self._countdown // 1000
