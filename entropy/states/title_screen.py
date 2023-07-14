from __future__ import annotations

import pygame as pg

import entropy
from entropy.components.button import TextButton
from entropy.components.text import Text
from entropy.states import State
from entropy.utils import Pos


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.background = entropy.assets.images.get("title-screen-bg")
        self.logo = entropy.assets.images.get("title-screen-logo-a")
        self.continue_btn = TitleScreenButton("CONTINUE", Pos(735, 550))
        self.new_game_btn = TitleScreenButton("NEW GAME", Pos(735, 630))
        self.settings_btn = TitleScreenButton("SETTINGS", Pos(735, 710))
        self.quit_btn = TitleScreenButton("QUIT", Pos(735, 790))

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self) -> None:
        self.continue_btn.update(mouse=self.control.mouse)
        self.new_game_btn.update(mouse=self.control.mouse)
        self.settings_btn.update(mouse=self.control.mouse)
        self.quit_btn.update(mouse=self.control.mouse)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
        surface.blit(self.logo, (660, 230))
        self.continue_btn.draw(surface=surface)
        self.new_game_btn.draw(surface=surface)
        self.settings_btn.draw(surface=surface)
        self.quit_btn.draw(surface=surface)


class TitleScreenButton(TextButton):
    def __init__(self, text: str, pos: Pos) -> None:
        font = entropy.assets.fonts.get("LanaPixel", "small")
        super().__init__(
            text=Text(text=text, font=font, color=pg.Color(6, 0, 9)),
            text_hover=Text(text=text, font=font, color=pg.Color(246, 255, 246)),
            image=entropy.assets.images.get("main-menu-btn"),
            image_hover=entropy.assets.images.get("main-menu-btn-hover"),
            pos=pos,
            sound_hover=entropy.assets.sound.get("hover"),
        )
