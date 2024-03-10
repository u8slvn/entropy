from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
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
from entropy.gui.component.button import Button
from entropy.gui.widgets.background import ImageBackground
from entropy.gui.widgets.menu import MenuGroup
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control

config = get_config()


def test_lang() -> None:
    translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._covered = False
        self._background = ImageBackground(name="title-screen-bg")
        self._logo = assets.image.get("title-screen-logo-a")
        # self._main_menu = self._build_menu()
        self._music = "main-theme"
        Button(
            self.sprites,
            image=assets.gui.get("main-menu-button-sheet-a"),
            focus_sound="hover",
            click_sound="click",
            action=test_lang,
            text="text",
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            topleft=(0, 200),
        )

    def setup(self) -> None:
        if mixer.currently_playing != self._music:
            mixer.play_music(name="main-theme")

        translator.set_translation(config.locale, domain="base")
        self._covered = False
        # self._main_menu.setup()

    def process_event(self, event: Event) -> None:
        ...
        # self._main_menu.process_event(event=event)

    def update(self, dt: float) -> None:
        super().update(dt)
        # self._main_menu.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)
        super().draw(surface)
        if self._covered is False:
            surface.blit(self._logo, (660, 0))
            # self._main_menu.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._covered = True

    def _build_menu(self) -> MenuGroup:
        menu_group = MenuGroup(parent=self._background)

        widgets: list[dict[str, Any]] = [
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
            button = self._build_menu_button(pos=pos, **widget)
            menu_group.add_widget(button)

        return menu_group

    def _build_menu_button(
        self, callback: Callable[[], None], text: str, pos: Pos
    ) -> Button:
        return Button(
            self.sprites,
            image=assets.gui.get("main-menu-button-sheet-a"),
            focus_sound="hover",
            click_sound="click",
            action=callback,
            text=text,
            text_color=GUI_BUTTON_TEXT_COLOR,
            text_font=assets.font.get(name=config.font, size=GUI_BUTTON_FONT_SIZE),
            topleft=pos,
        )
