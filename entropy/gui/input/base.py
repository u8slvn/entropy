from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pygame


class InputsBase(ABC):
    @abstractmethod
    def parse_event(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...
