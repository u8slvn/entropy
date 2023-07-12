from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Type


if TYPE_CHECKING:
    import pygame

    from entropy.misc.game import Game

states: dict[str, Type[State]] = {}


class State(ABC):
    def __init__(self, game: Game) -> None:
        self.game = game

    def __init_subclass__(cls, **kwargs):
        global states
        states[cls.__name__.upper()] = cls

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def process_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        ...

    @abstractmethod
    def teardown(self) -> None:
        ...
