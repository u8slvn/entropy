from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame as pg

import entropy

from entropy.components.button import TextButton
from entropy.components.menu import MenuButtonGroup
from entropy.components.text import Text
from entropy.states.base import State
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse


def test_lang():
    entropy.translator.set_translation("fr")


class TitleScreen(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self.background = entropy.assets.images.get("title-screen-bg")
        self.logo = entropy.assets.images.get("title-screen-logo-a")
        self.continue_btn = TitleScreenButton("CONTINUE", Pos(735, 550), test_lang)
        self.new_game_btn = TitleScreenButton("NEW GAME", Pos(735, 630), self.exit)
        self.settings_btn = TitleScreenButton(
            "SETTINGS", Pos(735, 710), self.on_click_settings
        )
        self.quit_btn = TitleScreenButton("QUIT", Pos(735, 790), self.on_click_quit)
        self.buttons = MenuButtonGroup(
            buttons=[
                self.continue_btn,
                self.new_game_btn,
                self.settings_btn,
                self.quit_btn,
            ]
        )

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, actions: Actions, mouse: Mouse) -> None:
        self.buttons.update(actions=actions, mouse=mouse)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
        surface.blit(self.logo, (660, 220))
        self.buttons.draw(surface=surface)

    def on_click_settings(self) -> None:
        self.control.transition_to("OverlayMenu")

    def on_click_quit(self) -> None:
        self.control.stop(delay=0.3)


class TitleScreenButton(TextButton):
    def __init__(self, text: str, pos: Pos, onclick: Callable[[], None]) -> None:
        font = entropy.assets.fonts.get("LanaPixel", "small")
        super().__init__(
            text=Text(text=text, font=font, color=pg.Color(6, 0, 9)),
            text_hover=Text(text=text, font=font, color=pg.Color(246, 255, 246)),
            image=entropy.assets.images.get("main-menu-btn"),
            image_hover=entropy.assets.images.get("main-menu-btn-hover"),
            sound_hover=entropy.assets.sound.get("hover"),
            sound_clicked=entropy.assets.sound.get("click"),
            onclick=onclick,
            pos=pos,
        )
