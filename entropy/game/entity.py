from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pygame

    from entropy.gui.input import Inputs


class GameEntity(ABC):
    """Informal Interface for all Game Entity"""

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    def process_inputs(self, inputs: Inputs) -> None:
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
