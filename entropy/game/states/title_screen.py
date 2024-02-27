from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame

from entropy import assets
from entropy import translator
from entropy.commands.game import QuitGame
from entropy.commands.state import ExitState
from entropy.commands.state import TransitionToNextState
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.game.states.base import State
from entropy.gui.components.background import ImageBackground
from entropy.gui.components.base import ALIGN
from entropy.gui.components.button import TextButton
from entropy.gui.components.menu import MenuGroup
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.components.base import Widget
    from entropy.gui.input import Inputs

config = get_config()


def test_lang():
    translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._covered = False
        self._background = ImageBackground(name="title-screen-bg")
        self._logo = assets.images.get("title-screen-logo-a")
        self._main_menu = self._build_menu()

    def setup(self) -> None:
        self._covered = False
        self._main_menu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._main_menu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._main_menu.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)
        if self._covered is False:
            surface.blit(self._logo, (660, 0))
            self._main_menu.draw(surface=surface)

    def teardown(self) -> None:
        self._covered = True

    def _build_menu(self) -> MenuGroup:
        menu_group = MenuGroup(parent=self._background)

        widgets = [
            {
                "parent": menu_group,
                "text": "CONTINUE",
                "callback": test_lang,
            },
            {
                "parent": menu_group,
                "text": "NEW GAME",
                "callback": ExitState(state=self),
            },
            {
                "parent": menu_group,
                "text": "SETTINGS",
                "callback": TransitionToNextState(
                    state=self, next_state="SettingsMenu"
                ),
            },
            {
                "parent": menu_group,
                "text": "QUIT",
                "callback": QuitGame(),
            },
        ]

        y = 400
        space_between = 100
        for i, widget in enumerate(widgets, start=1):
            pos = Pos(0, y + space_between * i)
            button = self._build_menu_button(**widget, pos=pos)
            menu_group.add_widget(button)

        return menu_group

    @staticmethod
    def _build_menu_button(
        parent: Widget, callback: Callable[[], None], text: str, pos: Pos
    ):
        return TextButton(
            parent=parent,
            image=assets.images.get("main-menu-button-sheet-a"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.fonts.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            text_align=ALIGN.CENTER,
            text_align_margin=Pos(0, 4),
            pos=pos,
        )
