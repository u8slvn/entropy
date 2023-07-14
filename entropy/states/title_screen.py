from __future__ import annotations

from typing import Callable

import pygame as pg

import entropy
from entropy.components.button import TextButton
from entropy.components.text import Text
from entropy.states import State
from entropy.utils import Pos


def action():
    print("clicked")


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.background = entropy.assets.images.get("title-screen-bg")
        self.logo = entropy.assets.images.get("title-screen-logo-a")
        self.continue_btn = TitleScreenButton("CONTINUE", Pos(735, 550), action)
        self.new_game_btn = TitleScreenButton("NEW GAME", Pos(735, 630), action)
        self.settings_btn = TitleScreenButton("SETTINGS", Pos(735, 710), action)
        self.quit_btn = TitleScreenButton("QUIT", Pos(735, 790), self.on_click_quit)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            self.control.mouse.hide()
            if event.key == pg.K_UP:
                pg.mouse.set_pos(self.continue_btn.rect.center)
            elif event.key == pg.K_DOWN:
                pg.mouse.set_pos(self.new_game_btn.rect.center)

    def update(self) -> None:
        self.continue_btn.update(mouse=self.control.mouse)  # type: ignore
        self.new_game_btn.update(mouse=self.control.mouse)  # type: ignore
        self.settings_btn.update(mouse=self.control.mouse)  # type: ignore
        self.quit_btn.update(mouse=self.control.mouse)  # type: ignore

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
        surface.blit(self.logo, (660, 220))
        self.continue_btn.draw(surface=surface)
        self.new_game_btn.draw(surface=surface)
        self.settings_btn.draw(surface=surface)
        self.quit_btn.draw(surface=surface)

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
