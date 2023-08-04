from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Self
from typing import Type


if TYPE_CHECKING:
    import pygame

    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse


class State(ABC):
    _states: dict[str : Type[Self]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control

    def __init_subclass__(cls):
        State._states[cls.__name__] = cls

    @classmethod
    def get_states(cls) -> dict[str : Type[Self]]:
        return cls._states

    def exit(self):
        self.control.state_stack.pop()

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, actions: Actions, mouse: Mouse) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...
