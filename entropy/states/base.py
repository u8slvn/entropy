from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pygame

    from entropy import Game


class State(ABC):
    def __init__(self, game: Game) -> None:
        self.game = game

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
    def draw(self, display: pygame.Surface) -> None:
        ...

    @abstractmethod
    def teardown(self) -> None:
        ...
