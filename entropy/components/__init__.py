from __future__ import annotations

from abc import ABC, abstractmethod

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


class ComponentRect:
    def __init__(self, x: int, y: int, rect: pygame.Rect) -> None:
        self.x = x
        self.y = y
        self.rect = rect
        self.scale_percent = ...
