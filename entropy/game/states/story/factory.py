from __future__ import annotations

from typing import TYPE_CHECKING

import entropy

from entropy.config import get_config
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.background import ImageBackground
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TypeWriterText
from entropy.utils import Color
from entropy.utils import Pos


config = get_config()


if TYPE_CHECKING:
    from entropy.gui.widgets.background import Background
    from entropy.gui.widgets.base import Widget


def build_background(params: str) -> Background:
    type_, value = params.split(":")

    match type_:
        case "color":
            return ColorBackground(color=Color(value))
        case "image":
            return ImageBackground(name=value)
        case _:
            raise ValueError(f"Unknown config type: '{type_}' for background.")


def build_event(parent: Widget, params: dict[str, str]) -> TypeWriterText:
    return TypeWriterText(
        parent=parent,
        font=entropy.assets.fonts.get("LanaPixel", "big"),
        text=params["value"],
        color="white",
        width=1700,
        speed=config.text_speed,
        pos=Pos(0, 700),
        align=Align(params["align"]),
    )
