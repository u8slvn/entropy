from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from entropy import window
from entropy.game.entity import GameEntity


if TYPE_CHECKING:
    from entropy.utils import Pos


class WidgetComponent(GameEntity, ABC):
    @abstractmethod
    def set_focus(self) -> None:
        ...

    @abstractmethod
    def unset_focus(self) -> None:
        ...

    @abstractmethod
    def has_focus(self) -> None:
        ...

    @abstractmethod
    def get_width(self) -> int:
        ...

    @abstractmethod
    def get_height(self) -> int:
        ...

    @abstractmethod
    def set_pos(self, pos: Pos, center_x: bool = False) -> int:
        ...

    def get_center_x(self) -> int:
        return (window.default_res.w - self.get_width()) // 2
