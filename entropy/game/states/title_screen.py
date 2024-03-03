from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame

from entropy import assets
from entropy import mixer
from entropy import translator
from entropy.commands.game import QuitGame
from entropy.commands.state import TransitionToNextState
from entropy.config import get_config
from entropy.constants import GUI_BUTTON_FONT_SIZE
from entropy.constants import GUI_BUTTON_TEXT_COLOR
from entropy.game.states.base import State
from entropy.gui.widgets.background import ImageBackground
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.button import TextButton
from entropy.gui.widgets.menu import MenuGroup
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs
    from entropy.gui.widgets.base import Widget

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
        self._music = "main-theme"

    def setup(self) -> None:
        if mixer.currently_playing != self._music:
            mixer.play_music(name="main-theme")
        translator.set_translation(config.locale, domain="base")
        self._covered = False
        self._main_menu.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._main_menu.process_inputs(inputs=inputs)

    def update(self, dt: float) -> None:
        self._main_menu.update(dt=dt)

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
            # {
            #     "text": "CONTINUE",
            #     "callback": test_lang,
            # },
            {
                "text": "NEW GAME",
                "callback": TransitionToNextState(state=self, next_state="Story"),
            },
            {
                "text": "SETTINGS",
                "callback": TransitionToNextState(
                    state=self, next_state="SettingsMenu"
                ),
            },
            {
                "text": "QUIT",
                "callback": QuitGame(),
            },
        ]

        y = 400
        space_between = 100
        for i, widget in enumerate(widgets, start=1):
            pos = Pos(0, y + space_between * i)
            button = self._build_menu_button(parent=menu_group, **widget, pos=pos)
            menu_group.add_widget(button)

        return menu_group

    @staticmethod
    def _build_menu_button(
        parent: Widget, callback: Callable[[], None], text: str, pos: Pos
    ) -> TextButton:
        return TextButton(
            parent=parent,
            image=assets.images.get("main-menu-button-sheet-a"),
            sound_focus="hover",
            sound_clicked="click",
            callback=callback,
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.fonts.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            text_align=Align.CENTER,
            text_align_margin=Pos(0, 4),
            pos=pos,
        )
