from __future__ import annotations

from enum import Enum
from enum import auto
from functools import partial
from typing import TYPE_CHECKING
from typing import Any

import pygame
import pygame as pg

from entropy import assets
from entropy.commands.display import DisableFullscreen
from entropy.commands.display import EnableFullscreen
from entropy.commands.locale import SwitchLocaleTo
from entropy.game.object import GameEntity
from entropy.game.states.base import State
from entropy.gui.components.background import ColorBackground
from entropy.gui.components.factory.menu import build_settings_menu
from entropy.gui.components.text import Text
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


class Submenu(Enum):
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
        self._submenu = self._build_submenu(Submenu.SETTINGS)

    def setup(self) -> None:
        self._submenu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE:
            self.exit()

        self._submenu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._submenu.update()

    def draw(self, surface: pg.Surface) -> None:
        if self.control.prev_state is not None:
            self.control.prev_state.draw(surface=surface)

        self._background.draw(surface=surface)
        self._submenu.draw(surface=surface)

    def teardown(self) -> None:
        self._submenu.teardown()

    def transition_to(self, submenu: Submenu):
        self._submenu.teardown()
        self._submenu = self._build_submenu(submenu=submenu)
        self._submenu.setup()

    def _build_submenu(self, submenu: Submenu) -> SettingsSubmenu:
        match submenu:
            case Submenu.DISPLAY:
                return SettingsSubmenu(
                    text="DISPLAY",
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
                            "callback": partial(self.transition_to, Submenu.SETTINGS),
                        },
                    ],
                )
            case Submenu.SOUND:
                return SettingsSubmenu(
                    text="SOUND",
                    config=[
                        {
                            "text": "BACK",
                            "callback": partial(self.transition_to, Submenu.SETTINGS),
                        },
                    ],
                )
            case Submenu.LANGUAGE:
                return SettingsSubmenu(
                    text="LANGUAGE",
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
                            "callback": partial(self.transition_to, Submenu.SETTINGS),
                        },
                    ],
                )
            case Submenu.DIALOGUE:
                return SettingsSubmenu(
                    text="DIALOGUE",
                    config=[
                        {
                            "text": "BACK",
                            "callback": partial(self.transition_to, Submenu.SETTINGS),
                        },
                    ],
                )
            case _:
                return SettingsSubmenu(
                    text="SETTINGS",
                    config=[
                        {
                            "text": "DISPLAY",
                            "callback": partial(self.transition_to, Submenu.DISPLAY),
                        },
                        {
                            "text": "SOUND",
                            "callback": partial(self.transition_to, Submenu.SOUND),
                        },
                        {
                            "text": "LANGUAGE",
                            "callback": partial(self.transition_to, Submenu.LANGUAGE),
                        },
                        {
                            "text": "DIALOGUE",
                            "callback": partial(self.transition_to, Submenu.DIALOGUE),
                        },
                        {
                            "text": "BACK",
                            "callback": self.exit,
                        },
                    ],
                )


class SettingsSubmenu(GameEntity):
    def __init__(self, text: str, config: list[dict[str, Any]]):
        font = assets.fonts.get("LanaPixel", "settings")
        self._title = Text(text=text, font=font, color="white")
        self._menu = build_settings_menu(config=config)

    def setup(self) -> None:
        self._title.setup()
        self._menu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._title.process_inputs(inputs=inputs)
        self._menu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._title.update()
        self._menu.update()

    def draw(self, surface: pygame.Surface) -> None:
        x = (surface.get_width() - self._title.width) // 2
        y = 200
        self._title.set_pos(Pos(x, y))
        self._title.draw(surface=surface)
        self._menu.draw(surface=surface)

    def teardown(self) -> None:
        self._title.teardown()
        self._menu.teardown()
