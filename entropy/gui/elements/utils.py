from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Literal


if TYPE_CHECKING:
    from entropy.gui.elements.base import UIElement


def move(
    items: list[UIElement],
    direction: Literal["vertical", "horizontal"],
    space_between: int,
    **kwargs: Any,
) -> None:
    for i, item in enumerate(items):
        item.move(**kwargs)
        if direction == "vertical":
            x = item.rect.left
            y = item.rect.top + space_between * i + item.rect.h * i + 1
            item.move(topleft=(x, y))
        else:
            x = item.rect.left + space_between * i + item.rect.w * i + 1
            y = item.rect.top
            item.move(topleft=(x, y))
