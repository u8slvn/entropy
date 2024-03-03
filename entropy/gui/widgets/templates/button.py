from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING
from typing import Callable

from entropy import assets
from entropy.config import get_config
from entropy.gui.widgets.button import Button
from entropy.gui.widgets.button import ObserverButton
from entropy.gui.widgets.button import TextButton
from entropy.gui.widgets.text import TText
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.widgets.button import AttrObserver


config = get_config()


SettingsButton = partial(
    TextButton,
    image=assets.image.get("settings-button-sheet"),
    sound_focus="hover",
    sound_clicked="click",
)

ConfigSettingsButton = partial(
    ObserverButton,
    image=assets.image.get("settings-button-sheet"),
    sound_focus="hover",
    sound_clicked="click",
)


def build_settings_button(
    text: str,
    pos: Pos,
    callback: Callable[[], None],
    attr_observer: AttrObserver | None = None,
) -> Button:
    font = assets.font.get("LanaPixel", "small")
    if attr_observer is not None:
        return ObserverButton(
            text=TText(text=text, font=font, color=Color("white")),
            image=assets.image.get("settings-button-sheet"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            pos=pos,
            attr_observer=attr_observer,
        )
    else:
        return TextButton(
            image=assets.image.get("settings-button-sheet"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            pos=pos,
            text=TText(text=text, font=font, color=Color("white")),
        )
