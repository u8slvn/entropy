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
from entropy.gui.elements.background import ImageBackground
from entropy.gui.elements.base import UIElement
from entropy.gui.elements.base import UIElementGroup
from entropy.gui.elements.button import Button
from entropy.gui.elements.menu import Menu
from entropy.gui.elements.utils import move


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control

config = get_config()


def test_lang() -> None:
    translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.ui_elements = UIElementGroup()
        self._covered = False
        self._background = ImageBackground(name="title-screen-bg")
        self._logo = assets.image.get("title-screen-logo-a")
        self._main_menu = self._build_menu()
        self._music = "main-theme"

    def setup(self) -> None:
        if mixer.currently_playing != self._music:
            mixer.play_music(name="main-theme")

        translator.set_translation(config.locale, domain="base")
        self._covered = False

    def process_event(self, event: Event) -> None:
        self.ui_elements.process_event(event)
        self._main_menu.process_event(event=event)

    def update(self, dt: float) -> None:
        self.ui_elements.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)

        if self._covered is False:
            self.ui_elements.draw(surface)
            surface.blit(self._logo, (660, 0))

    def teardown(self) -> None:
        super().teardown()
        self._covered = True

    def exit(self) -> None:
        self.ui_elements.cleanup()
        super().exit()

    def _build_menu(self) -> Menu:
        items: list[UIElement] = [
            self._build_menu_button(
                text="NEW GAME",
                action=TransitionToNextState(state=self, next_state="Story"),
            ),
            self._build_menu_button(
                text="SETTINGS",
                action=TransitionToNextState(state=self, next_state="SettingsMenu"),
            ),
            self._build_menu_button(
                text="QUIT",
                action=QuitGame(),
            ),
        ]
        move(items=items, space_between=40, direction="vertical", topleft=(0, 400))
        return Menu(items=items, direction="vertical")

    def _build_menu_button(
        self,
        action: Callable[[], None],
        text: str,
    ) -> Button:
        return Button(
            self.ui_elements,
            image=assets.gui.get("main-menu-button-sheet-a"),
            focus_sound="hover",
            click_sound="click",
            action=action,
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
        )
