from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.event.event import Event
from entropy.game.entity import GameEntity
from entropy.logging import get_logger


if TYPE_CHECKING:
    import pygame


logger = get_logger()


class Node(GameEntity):
    """Node class: Represent a node of the game story."""

    def __init__(self, next_id: str) -> None:
        super().__init__()
        self.next_id = next_id
        self.done = False

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass


class NullNode(Node):
    """Null node class: Represent a null node of the game story."""

    def __init__(self) -> None:
        super().__init__(next_id="null")

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass
