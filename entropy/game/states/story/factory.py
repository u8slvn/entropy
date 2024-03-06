from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable
from typing import Generator

import entropy

from entropy.config import get_config
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.background import ImageBackground
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TypeWriterText
from entropy.utils import Color
from entropy.utils import Pos


config = get_config()

if TYPE_CHECKING:
    from entropy.gui.transistions.base import Transition
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


def build_event(
    parent: Widget, params: dict[str, str]
) -> Generator[TypeWriterText, None, None]:
    for value in params["values"]:
        align = Align(params["align"]) if params.get("align") else None
        yield TypeWriterText(
            parent=parent,
            font=entropy.assets.font.get("LanaPixel", "medium"),
            text=value,
            color="white",
            width=1700,
            speed=config.text_speed,
            voice=params["voice"],
            pos=Pos(113, 700),
            align=align,
        )


def build_transition(
    params: dict[str, str | int], callback: Callable[[], None]
) -> Transition:
    match params["type"]:
        case "fade-in":
            return FadeIn(duration=params["duration"], callback=callback)
        case "fade-out":
            return FadeOut(duration=params["duration"], callback=callback)
        case _:
            raise NotImplementedError
