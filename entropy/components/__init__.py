from __future__ import annotations

from abc import ABC, abstractmethod

import pygame.event


class Component(ABC):
    position: tuple[int, int]

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def draw(self, display: pygame.Surface) -> None:
        ...
