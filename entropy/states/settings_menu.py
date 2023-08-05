from __future__ import annotations

from collections import OrderedDict
from enum import Enum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING

import pygame as pg

from entropy import assets
from entropy import translator
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.factory.menu import build_main_menu
from entropy.gui.components.text import Text
from entropy.states.base import State
from entropy.utils import Color


if TYPE_CHECKING:
    from entropy.gui.input.keyboard_events import KeyboardEvents
    from entropy.gui.input.mouse_events import MouseEvents
    from entropy.misc.control import Control


class MenuState(Enum):
    SETTINGS = auto()
    DISPLAY = auto()
    SOUND = auto()
    LANGUAGE = auto()
    TEXT = auto()


class SettingsMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._background = ColorBackground(color=Color(0, 0, 0, 200))
        self._font = assets.fonts.get("LanaPixel", "big")
        self.transition_to(state=MenuState.SETTINGS)

    def update(self, keyboard_e: KeyboardEvents, mouse_e: MouseEvents) -> None:
        if keyboard_e.SPACE:
            self.exit()

        self._menu.update(keyboard_e=keyboard_e, mouse_e=mouse_e)

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface=surface)

        surface.blit(self._background, self._background.pos)
        x = (surface.get_width() - self._title.surface.get_width()) // 2
        y = 200
        surface.blit(self._title.surface, (x, y))
        self._menu.draw(surface=surface)

    def transition_to(self, state: MenuState):
        if state == MenuState.DISPLAY:
            title = "DISPLAY"
            config = OrderedDict(
                {
                    "BACK": partial(self.transition_to, MenuState.SETTINGS),
                }
            )
        elif state == MenuState.SOUND:
            title = "SOUND"
            config = OrderedDict(
                {
                    "BACK": partial(self.transition_to, MenuState.SETTINGS),
                }
            )
        elif state == MenuState.LANGUAGE:
            title = "LANGUAGE"
            config = OrderedDict(
                {
                    "ENGLISH": partial(translator.set_translation, "en"),
                    "FRENCH": partial(translator.set_translation, "fr"),
                    "BACK": partial(self.transition_to, MenuState.SETTINGS),
                }
            )
        elif state == MenuState.TEXT:
            title = "TEXT"
            config = OrderedDict(
                {
                    "BACK": partial(self.transition_to, MenuState.SETTINGS),
                }
            )

        else:
            title = "SETTINGS"
            config = OrderedDict(
                {
                    "DISPLAY": partial(self.transition_to, MenuState.DISPLAY),
                    "SOUND": partial(self.transition_to, MenuState.SOUND),
                    "LANGUAGE": partial(self.transition_to, MenuState.LANGUAGE),
                    "TEXT": partial(self.transition_to, MenuState.TEXT),
                    "BACK": self.exit,
                }
            )

        self._title = Text(text=title, font=self._font, color="white")
        self._menu = build_main_menu(config=config)
