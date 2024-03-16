from __future__ import annotations

from abc import ABC
from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Callable
from typing import final

from entropy.game.entity import GameEntity
from entropy.tools.timer import Timer


if TYPE_CHECKING:
    from entropy.event.event import Event


@final
class Ease(IntEnum):
    IN = 0
    OUT = 1


class Transition(GameEntity, ABC):
    _ease: Ease

    def __init__(
        self,
        duration: int,
        callback: Callable[[], None] | None = None,
    ) -> None:
        autostart = self._ease is Ease.IN
        self._timer = Timer(
            duration=duration,
            callback=callback,
            autostart=autostart,
        )
        self._active = False

    def activate(self) -> None:
        self._active = True
        self._timer.start()

    def is_active(self) -> bool:
        return self._active

    def setup(self) -> None:
        self._timer.setup()
        if self._timer.is_started():
            self._active = True

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self._timer.update(dt=dt)

        if self._timer.is_done() or not self._timer.is_started():
            self._active = False
