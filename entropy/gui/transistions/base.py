from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Callable
from typing import final

from entropy.tools.timer import Timer
from entropy.utils import Pos


if TYPE_CHECKING:
    import pygame

    from entropy.utils import Size


@final
class Ease(IntEnum):
    IN = 0
    OUT = 1


class Transition(Timer, ABC):
    _ease: Ease

    def __init__(
        self,
        size: Size,
        duration: int,
        callback: Callable[[], None] | None = None,
    ) -> None:
        autostart = True if self._ease is Ease.IN else False
        super().__init__(
            duration=duration,
            callback=callback,
            autostart=autostart,
        )
        self._size = size

        self._pos = Pos(0, 0)

    @abstractmethod
    def _update(self) -> None:
        pass

    def update(self) -> None:
        super().update()
        if self.is_done() or not self.is_started():
            return

        self._update()

    @abstractmethod
    def _draw(self, surface: pygame.Surface) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_done() or not self.is_started():
            return

        self._draw(surface=surface)
