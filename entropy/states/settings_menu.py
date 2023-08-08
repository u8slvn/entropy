from __future__ import annotations

from enum import Enum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING

import pygame as pg

from entropy import assets
from entropy.commands.display import DisableFullscreen
from entropy.commands.display import EnableFullscreen
from entropy.commands.locale import SwitchLocaleTo
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.factory.menu import build_settings_menu
from entropy.gui.components.text import Text
from entropy.states.base import State
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.input.keyboard_inputs import KeyboardInputs
    from entropy.gui.input.mouse_inputs import MouseInputs
    from entropy.misc.control import Control


class MenuState(Enum):
    SETTINGS = auto()
    DISPLAY = auto()
    SOUND = auto()
    LANGUAGE = auto()
    DIALOGUE = auto()


class SettingsMenu(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._background = ColorBackground(color=Color(0, 0, 0, 150))
        self._font = assets.fonts.get("LanaPixel", "settings")
        self.transition_to(state=MenuState.SETTINGS)

    def update(self, keyboard_e: KeyboardInputs, mouse_e: MouseInputs) -> None:
        if keyboard_e.SPACE:
            self.exit()

        self._menu.update(keyboard_e=keyboard_e, mouse_e=mouse_e)

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface=surface)

        self._background.draw(surface=surface)
        x = (surface.get_width() - self._title.width) // 2
        y = 200
        self._title.set_pos(Pos(x, y))
        self._title.draw(surface=surface)
        self._menu.draw(surface=surface)

    def transition_to(self, state: MenuState):
        if state == MenuState.DISPLAY:
            self._title = Text(text="DISPLAY", font=self._font, color="white")
            self._menu = build_settings_menu(
                config=[
                    {
                        "text": "FULLSCREEN",
                        "callback": EnableFullscreen(),
                        "watch": "fullscreen",
                        "match": True,
                    },
                    {
                        "text": "FRAMED",
                        "callback": DisableFullscreen(),
                        "watch": "fullscreen",
                        "match": False,
                    },
                    {
                        "text": "BACK",
                        "callback": partial(self.transition_to, MenuState.SETTINGS),
                    },
                ],
            )

        elif state == MenuState.SOUND:
            self._title = Text(text="SOUND", font=self._font, color="white")
            self._menu = build_settings_menu(
                config=[
                    {
                        "text": "BACK",
                        "callback": partial(self.transition_to, MenuState.SETTINGS),
                    },
                ],
            )

        elif state == MenuState.LANGUAGE:
            self._title = Text(text="LANGUAGE", font=self._font, color="white")
            self._menu = build_settings_menu(
                config=[
                    {
                        "text": "ENGLISH",
                        "callback": SwitchLocaleTo(locale="en"),
                        "watch": "locale",
                        "match": "en",
                    },
                    {
                        "text": "FRANÇAIS",
                        "callback": SwitchLocaleTo(locale="fr"),
                        "watch": "locale",
                        "match": "fr",
                    },
                    {
                        "text": "BACK",
                        "callback": partial(self.transition_to, MenuState.SETTINGS),
                    },
                ],
            )

        elif state == MenuState.DIALOGUE:
            self._title = Text(text="DIALOGUE", font=self._font, color="white")
            self._menu = build_settings_menu(
                config=[
                    {
                        "text": "BACK",
                        "callback": partial(self.transition_to, MenuState.SETTINGS),
                    },
                ],
            )

        else:
            self._title = Text(text="SETTINGS", font=self._font, color="white")
            self._menu = build_settings_menu(
                config=[
                    {
                        "text": "DISPLAY",
                        "callback": partial(self.transition_to, MenuState.DISPLAY),
                    },
                    {
                        "text": "SOUND",
                        "callback": partial(self.transition_to, MenuState.SOUND),
                    },
                    {
                        "text": "LANGUAGE",
                        "callback": partial(self.transition_to, MenuState.LANGUAGE),
                    },
                    {
                        "text": "DIALOGUE",
                        "callback": partial(self.transition_to, MenuState.DIALOGUE),
                    },
                    {
                        "text": "BACK",
                        "callback": self.exit,
                    },
                ],
            )
