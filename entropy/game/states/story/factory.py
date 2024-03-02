from __future__ import annotations

from entropy.gui.widgets.background import ColorBackground
from entropy.utils import Color


def build_background(config: str):
    type_, value = config.split(":")

    match type_:
        case "color":
            return ColorBackground(Color(value))
