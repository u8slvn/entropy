from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Literal


if TYPE_CHECKING:
    from entropy.gui.component.base import Sprite


def move(
    items: list[Sprite],
    space_between: int,
    direction: Literal["vertical", "horizontal"],
    **kwargs: Any,
) -> None:
    for i, button in enumerate(items):
        button.move(**kwargs)
        if direction == "vertical":
            x = button.rect.left
            y = button.rect.top + space_between * i + button.rect.h * i + 1
            button.move(topleft=(x, y))
        else:
            x = button.rect.left + space_between * i + button.rect.w * i + 1
            y = button.rect.top
            button.move(topleft=(x, y))
