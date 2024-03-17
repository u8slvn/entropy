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
    """State class. Represent a state of the game."""

    _states: ClassVar[dict[str, Type[State]]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control

    def __init_subclass__(cls) -> None:
        State._states[cls.get_name()] = cls

    @classmethod
    def get_name(cls) -> str:
        """Return the name of the state."""
        return cls.__name__

    @classmethod
    def get_states(cls) -> dict[str, Type[State]]:
        """Return the available states of the game."""
        return cls._states

    def transition_to(self, state_name: str, with_exit: bool = False) -> None:
        """Transition to another state.
        If with_exit is True, the current state will be exited.
        """
        self.control.transition_to(state_name=state_name, with_exit=with_exit)

    def teardown(self) -> None:
        """Teardown the state."""
        pass
        # self.control.event_manager.flush()

    def exit(self) -> None:
        """Exit the state."""
        self.teardown()
        self.control.state_stack.pop()
        self.control.current_state.setup()
        logger.info(f'Game state changed to "{self.control.current_state.get_name()}".')

    def __repr__(self) -> str:
        return f"State<{self.get_name()}>"
