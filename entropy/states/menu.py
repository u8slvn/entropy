from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

import entropy
from entropy.colors import BLACK, WHITE
from entropy.components.background import Background
from entropy.components.button import Button
from entropy.states import State


if TYPE_CHECKING:
    from entropy.misc.game import Game


class Menu(State):
    position = (0, 100)

    def __init__(self, game: Game):
        super().__init__(game=game)
        self.bg = Background("menu-bg")
        self.button = Button(
            text="hello",
            font=entropy.assets.fonts.get("LanaPixel", 20),
            color=BLACK,
            color_hover=WHITE,
            image=entropy.assets.images.get("main-menu-btn"),
            image_hover=entropy.assets.images.get("main-menu-btn-hover"),
            x=600,
            y=600,
        )
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button)

    def setup(self) -> None:
        self.button.re_scale()

    def process_event(self, event: pygame.event.Event) -> None:
        ...

    def update(self) -> None:
        self.buttons.update()

    def draw(self, display: pygame.Surface) -> None:
        self.bg.draw(display=display)
        self.buttons.draw(display)

    def teardown(self) -> None:
        pass
