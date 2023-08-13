from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from entropy import assets
from entropy import translator
from entropy.commands.game import QuitGame
from entropy.commands.state import ExitState
from entropy.commands.state import TransitionToNextState
from entropy.game.states.base import State
from entropy.gui.components.menu import MenuWidgetGroup
from entropy.gui.components.templates.button import TitleScreenButton
from entropy.gui.components.templates.text import ButtonText
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs


def test_lang():
    translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._covered = False
        self._background = assets.images.get("title-screen-bg")
        self._logo = assets.images.get("title-screen-logo-a")
        self._main_menu = self._build_main_menu()

    def setup(self) -> None:
        self._covered = False

    def process_inputs(self, inputs: Inputs) -> None:
        self._main_menu.process_inputs(inputs=inputs)

    def update(self) -> None:
        self._main_menu.update()

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._background, (0, 0))
        if self._covered is False:
            surface.blit(self._logo, (660, 0))
            self._main_menu.draw(surface=surface)

    def teardown(self) -> None:
        self._covered = True

    def _build_main_menu(self) -> MenuWidgetGroup:
        widgets = [
            TitleScreenButton(text=ButtonText("CONTINUE"), callback=test_lang),
            TitleScreenButton(text=ButtonText("NEW GAME"), callback=ExitState(self)),
            TitleScreenButton(
                text=ButtonText("SETTINGS"),
                callback=TransitionToNextState(state=self, next_state="SettingsMenu"),
            ),
            TitleScreenButton(text=ButtonText("QUIT"), callback=QuitGame()),
        ]
        return MenuWidgetGroup(pos=Pos(0, 400), margin=20, widgets=widgets)
