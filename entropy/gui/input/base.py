from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pygame


class InputsController(ABC):
    @abstractmethod
    def parse_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def flush(self) -> None: ...
