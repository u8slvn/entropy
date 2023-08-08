from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Type

from entropy.commands.base import Commands


if TYPE_CHECKING:
    import pygame

    from entropy.gui.input import Inputs
    from entropy.misc.control import Control


class State(ABC):
    _states: dict[str, Type[State]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control
        self._commands = Commands()

    def __init_subclass__(cls):
        State._states[cls.__name__] = cls

    @classmethod
    def get_states(cls) -> dict[str, Type[State]]:
        return cls._states

    def exit(self) -> None:
        self.control.state_stack.pop()
        self.control.current_state.setup()

    def setup(self) -> None:
        pass

    @abstractmethod
    def process_inputs(self, inputs: Inputs) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...

    def teardown(self) -> None:
        pass
