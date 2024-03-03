from __future__ import annotations

from typing import TYPE_CHECKING

import entropy

from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.background import ImageBackground
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TypeWriterText
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.gui.widgets.background import Background
    from entropy.gui.widgets.base import Widget


def build_background(config: str) -> Background:
    type_, value = config.split(":")

    match type_:
        case "color":
            return ColorBackground(color=Color(value))
        case "image":
            return ImageBackground(name=value)
        case _:
            raise ValueError(f"Unknown config type: '{type_}' for background.")


def build_event(parent: Widget, config: dict[str, str]) -> TypeWriterText:
    return TypeWriterText(
        parent=parent,
        font=entropy.assets.fonts.get("LanaPixel", "big"),
        text=config["value"],
        color="red",
        width=600,
        speed=1.4,
        align=Align(config["align"]),
    )
