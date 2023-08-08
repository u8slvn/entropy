from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from entropy import assets
from entropy import translator
from entropy.commands.game import QuitGame
from entropy.commands.state import ExitState
from entropy.commands.state import TransitionToNextState
from entropy.gui.components.factory.menu import build_main_menu
from entropy.gui.components.menu import MenuButtonGroup
from entropy.states.base import State


if TYPE_CHECKING:
    from entropy.gui.input import Inputs
    from entropy.misc.control import Control


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

    def update(self, dt: float) -> None:
        self._main_menu.update()

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._background, (0, 0))
        if self._covered is False:
            surface.blit(self._logo, (660, 0))
            self._main_menu.draw(surface=surface)

    def teardown(self) -> None:
        self._covered = True

    def _build_main_menu(self) -> MenuButtonGroup:
        return build_main_menu(
            config=[
                {
                    "text": "CONTINUE",
                    "callback": test_lang,
                },
                {
                    "text": "NEW GAME",
                    "callback": ExitState(self),
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
        )
