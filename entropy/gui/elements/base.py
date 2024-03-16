from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any

import pygame as pg


if TYPE_CHECKING:
    from entropy.event.event import Event


class UIElementBase(ABC):
    @abstractmethod
    def process_event(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        raise NotImplementedError

    def cleanup(self) -> None:
        pass


class UIElement(UIElementBase, ABC):
    def __init__(self, group: UIElementGroup | None):
        group.add(self)
        self.image: pg.Surface | None = None
        self.rect: pg.rect.Rect | None = None

    def process_event(self, event: Event) -> None:
        pass

    def move(self, **kwargs: Any) -> None:
        if self.image is not None:
            self.rect = self.image.get_rect(**kwargs)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)

    def cleanup(self) -> None:
        pass


class UIElementGroup(UIElementBase):
    def __init__(self, elements: list[UIElement] | None = None) -> None:
        self.elements = elements or []

    def add(self, *elements: Any) -> None:
        self.elements.append(*elements)

    def process_event(self, event: Event) -> None:
        for element in self.elements:
            element.process_event(event)

    def update(self, **kwargs: Any) -> None:
        for element in self.elements:
            element.update(**kwargs)

    def draw(self, surface: pg.Surface) -> None:
        for element in self.elements:
            element.draw(surface)

    def cleanup(self) -> None:
        for element in self.elements:
            element.cleanup()

    def empty(self) -> None:
        self.elements = []
