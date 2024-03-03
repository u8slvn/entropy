from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame

from entropy.game.entity import GameEntity


if TYPE_CHECKING:
    from entropy.gui.input import Inputs


class Timer(GameEntity):
    """Simple timer object in millisecond."""

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
        self._trigger_callback()

    def is_started(self) -> bool:
        return self._started

    def is_done(self) -> bool:
        return self._done

    def setup(self) -> None:
        if self._autostart is True:
            self.start()

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self, dt: float) -> None:
        if self.is_done() or not self.is_started():
            return

        ticks = pygame.time.get_ticks() - self._start_ticks
        self._countdown = self._duration - ticks
        if self._countdown <= 0:
            self.stop()

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        self._countdown = self._duration
        self._start_ticks = 0
        self._started = False
        self._done = False


class TimerSecond(Timer):
    """Simple timer object in second."""

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
