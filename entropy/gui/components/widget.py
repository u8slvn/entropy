from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from entropy.gui.components.base import Widget


if TYPE_CHECKING:
    from entropy.utils import Pos


class WidgetComponent(Widget, ABC):
    @abstractmethod
    def set_focus(self) -> None: ...

    @abstractmethod
    def unset_focus(self) -> None: ...

    @abstractmethod
    def has_focus(self) -> None: ...

    @abstractmethod
    def get_width(self) -> int: ...

    @abstractmethod
    def get_height(self) -> int: ...

    @abstractmethod
    def set_pos(self, pos: Pos) -> int: ...
