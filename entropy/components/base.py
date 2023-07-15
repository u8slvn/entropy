from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pygame.event


class Component(ABC):
    position: tuple[int, int]

    def handle_event(self, event: pygame.event.Event) -> None:
        return

    def update(self) -> None:
        return

    @abstractmethod
    def draw(self, display: pygame.Surface) -> None:
        ...
