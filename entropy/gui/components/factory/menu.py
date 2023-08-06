from __future__ import annotations

from typing import Any

from entropy.gui.components.factory.button import build_settings_button
from entropy.gui.components.factory.button import build_title_screen_button
from entropy.gui.components.menu import MenuButtonGroup
from entropy.utils import Pos


def build_main_menu(config: list[dict[str, Any]]) -> MenuButtonGroup:
    buttons = []
    x = 0
    y = 400
    h = 100

    for params in config:
        pos = Pos(x, y)
        button = build_title_screen_button(**params, pos=pos)
        buttons.append(button)
        y += h

    return MenuButtonGroup(buttons=buttons)


def build_settings_menu(config: list[dict[str, Any]]) -> MenuButtonGroup:
    *config, last_config = config
    buttons = []
    x = 735
    y = 310
    h = 80

    for params in config:
        pos = Pos(x, y)
        button = build_settings_button(**params, pos=pos)
        buttons.append(button)
        y += h

    exit_button = build_settings_button(**last_config, pos=Pos(x, 790))
    buttons.append(exit_button)

    return MenuButtonGroup(buttons=buttons)
