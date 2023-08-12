from __future__ import annotations

from typing import Any
from typing import Callable

from entropy import assets
from entropy.gui.components.button import Button
from entropy.gui.components.button import ConfigObserverButton
from entropy.gui.components.text import Text
from entropy.utils import Color
from entropy.utils import Pos


def build_title_screen_button(
    text: str, pos: Pos, callback: Callable[[], None]
) -> Button:
    font = assets.fonts.get("LanaPixel", "small")
    return Button(
        text=Text(text=text, font=font, color=Color("white")),
        image=assets.images.get("main-menu-button-sheet-a"),
        sound_focus="hover",
        sound_clicked="click",
        callback=callback,
        pos=pos,
        padding=Pos(0, 4),
    )


def build_settings_button(
    text: str,
    pos: Pos,
    callback: Callable[[], None],
    watch: str | None = None,
    match: Any | None = None,
) -> Button:
    font = assets.fonts.get("LanaPixel", "small")
    if watch is not None and match is not None:
        return ConfigObserverButton(
            text=Text(text=text, font=font, color=Color("white")),
            image=assets.images.get("settings-button-sheet"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            pos=pos,
            watch=watch,
            match=match,
        )
    else:
        return Button(
            text=Text(text=text, font=font, color=Color("white")),
            image=assets.images.get("settings-button-sheet"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            pos=pos,
        )
