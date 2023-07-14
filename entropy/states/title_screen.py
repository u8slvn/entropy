from __future__ import annotations

import pygame as pg

import entropy
from entropy.components.button import TitleScreenButton
from entropy.states import State
from entropy.utils import Pos


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.background = entropy.assets.images.get("menu-bg")
        self.continue_btn = TitleScreenButton("CONTINUE", Pos(0, 30))
        self.new_game_btn = TitleScreenButton("NEW GAME", Pos(0, 300))
        self.settings_btn = TitleScreenButton("SETTINGS", Pos(0, 600))
        self.quit_btn = TitleScreenButton("QUIT", Pos(0, 900))

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self) -> None:
        self.continue_btn.update(mouse=self.control.mouse)
        self.new_game_btn.update(mouse=self.control.mouse)
        self.settings_btn.update(mouse=self.control.mouse)
        self.quit_btn.update(mouse=self.control.mouse)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
        self.continue_btn.draw(surface=surface)
        self.new_game_btn.draw(surface=surface)
        self.settings_btn.draw(surface=surface)
        self.quit_btn.draw(surface=surface)
