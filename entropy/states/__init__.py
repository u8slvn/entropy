from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.states.base import State
from entropy.states.menu import Menu
from entropy.states.splash import Splash


if TYPE_CHECKING:
    from entropy.misc.game import Game

__all__ = ["State", "loads"]


def loads(game: Game) -> dict[str, State]:
    states = [Splash, Menu]

    return {state.__name__.upper(): state(game=game) for state in states}
