from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pygame as pg

    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse

__all__ = ["State"]


class State(ABC):
    def __init__(self, control: Control) -> None:
        self.control = control

    def exit(self):
        self.control.state_stack.pop()

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, actions: Actions, mouse: Mouse) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        ...
