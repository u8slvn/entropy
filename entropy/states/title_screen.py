from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.gui.components.factory.menu import build_main_menu
from entropy.gui.components.menu import MenuButtonGroup
from entropy.states.base import State


if TYPE_CHECKING:
    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents
    from entropy.misc.control import Control


def test_lang():
    entropy.translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._overlay = False
        self._background = entropy.assets.images.get("title-screen-bg")
        self._logo = entropy.assets.images.get("title-screen-logo-a")
        self._main_menu = self._build_main_menu()

    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        self._main_menu.update(keyboard_e=keyboard_e, mouse_e=mouse_e)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._background, (0, 0))
        if self._overlay is False:
            surface.blit(self._logo, (660, 220))
            self._main_menu.draw(surface=surface)

    def onclick_settings(self) -> None:
        self._overlay = True
        self.control.transition_to("OverlayMenu")

    def onclick_quit(self) -> None:
        self.control.stop(delay=0.3)

    def _build_main_menu(self) -> MenuButtonGroup:
        config = OrderedDict(
            {
                "CONTINUE": test_lang,
                "NEW GAME": self.exit,
                "SETTINGS": self.onclick_settings,
                "QUIT": self.onclick_quit,
            }
        )
        return build_main_menu(config=config)
