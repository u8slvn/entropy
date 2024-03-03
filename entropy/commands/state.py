from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.commands.base import Command


if TYPE_CHECKING:
    from entropy.game.states import State


class TransitionToNextState(Command):
    def __init__(self, state: State, next_state: str, with_exit: bool = False) -> None:
        self._state = state
        self._next_state = next_state
        self._with_exit = with_exit

    def __call__(self) -> None:
        self._state.transition_to(
            state_name=self._next_state, with_exit=self._with_exit
        )


class ExitState(Command):
    def __init__(self, state: State) -> None:
        self._state = state

    def __call__(self):
        self._state.exit()
