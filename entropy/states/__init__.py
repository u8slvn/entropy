from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type


if TYPE_CHECKING:
    import pygame as pg

    from entropy.game import Game

__all__ = ["State", "load"]


def load() -> dict[str, State]:
    # TODO: add auto load
    from entropy.states.menu import Menu  # noqa
    from entropy.states.splash import Splash  # noqa

    return {name.upper(): state() for name, state in State.states.items()}


class State(ABC):
    states: dict[str, Type[State]] = {}

    def __init__(self) -> None:
        self.game: Game | None = None

    def __init_subclass__(cls, **kwargs) -> None:
        State.states[cls.__name__] = cls

    def startup(self, game: Game) -> None:
        self.game = game

    def cleanup(self) -> None:
        self.game = None

    @abstractmethod
    def handle_event(self, event: pg.event.Event, mouse_pos: tuple[int, int]) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        ...
