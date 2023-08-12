from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from entropy.game.entity import GameEntity


class WidgetComponent(GameEntity, ABC):
    @abstractmethod
    def set_focus(self) -> None:
        ...

    @abstractmethod
    def unset_focus(self) -> None:
        ...

    @abstractmethod
    def width(self) -> int:
        ...

    @abstractmethod
    def height(self) -> int:
        ...
