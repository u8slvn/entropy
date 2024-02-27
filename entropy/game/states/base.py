from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Type

from entropy.game.entity import GameEntity
from entropy.logging import get_logger


if TYPE_CHECKING:
    from entropy.game.control import Control

logger = get_logger()


class State(GameEntity, ABC):
    _states: ClassVar[dict[str, Type[State]]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control

    def __init_subclass__(cls) -> None:
        State._states[cls.get_name()] = cls

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_states(cls) -> dict[str, Type[State]]:
        return cls._states

    def exit(self) -> None:
        self.teardown()
        self.control.state_stack.pop()
        self.control.current_state.setup()
        logger.info(f'Game state changed to "{self.control.current_state.get_name()}".')
