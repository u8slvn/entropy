from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Type


if TYPE_CHECKING:
    import pygame

    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents
    from entropy.misc.control import Control


class State(ABC):
    _states: dict[str, Type[State]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control

    def __init_subclass__(cls):
        State._states[cls.__name__] = cls

    @classmethod
    def get_states(cls) -> dict[str, Type[State]]:
        return cls._states

    def exit(self):
        self.control.state_stack.pop()

    @abstractmethod
    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...
