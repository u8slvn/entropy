from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

from entropy.gui.components.factory.button import build_settings_button
from entropy.gui.components.factory.button import build_title_screen_button
from entropy.gui.components.menu import MenuButtonGroup
from entropy.utils import Pos


if TYPE_CHECKING:
    from collections import OrderedDict


def build_main_menu(config: OrderedDict[str, Callable[[], None]]) -> MenuButtonGroup:
    *config, last_config = config.items()
    buttons = []
    x = 0
    y = 550
    h = 80

    for text, callback in config:
        pos = Pos(x, y)
        button = build_title_screen_button(text=text, pos=pos, callback=callback)
        buttons.append(button)
        y += h

    text, callback = last_config
    exit_button = build_title_screen_button(
        text=text,
        pos=Pos(x, 790),
        callback=callback,
    )
    buttons.append(exit_button)

    return MenuButtonGroup(buttons=buttons)


def build_settings_menu(
    config: OrderedDict[str, Callable[[], None]]
) -> MenuButtonGroup:
    *config, last_config = config.items()
    buttons = []
    x = 735
    y = 310
    h = 80

    for text, callback in config:
        pos = Pos(x, y)
        button = build_settings_button(text=text, pos=pos, callback=callback)
        buttons.append(button)
        y += h

    text, callback = last_config
    exit_button = build_settings_button(
        text=text,
        pos=Pos(x, 790),
        callback=callback,
    )
    buttons.append(exit_button)

    return MenuButtonGroup(buttons=buttons)
