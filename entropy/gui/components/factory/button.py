from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

from entropy import assets
from entropy.gui.components.button import Button
from entropy.gui.components.text import Text
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.utils import Pos


def build_title_screen_button(
    text: str, pos: Pos, callback: Callable[[], None]
) -> Button:
    font = assets.fonts.get("LanaPixel", "small")
    return Button(
        text=Text(text=text, font=font, color=Color(0, 0, 0)),
        text_focus=Text(text=text, font=font, color=Color(255, 255, 255)),
        image=assets.images.get("main-menu-btn"),
        image_focus=assets.images.get("main-menu-btn-hover"),
        sound_focus=assets.sound.get("hover"),
        sound_clicked=assets.sound.get("click"),
        callback=callback,
        pos=pos,
    )
