from __future__ import annotations

from typing import TYPE_CHECKING

import entropy
from entropy.components.button import Button
from entropy.states import State
from entropy.utils import Pos


if TYPE_CHECKING:
    import pygame as pg


class TitleScreen(State):
    position = (0, 100)

    def __init__(self):
        super().__init__()
        self.background = entropy.assets.images.get("menu-bg")
        self.button = Button(
            image=entropy.assets.images.get("main-menu-btn"),
            image_hover=entropy.assets.images.get("main-menu-btn-hover"),
            pos=Pos(0, 200),
            sound_hover=entropy.assets.sound.get("hover"),
        )

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self) -> None:
        self.button.update(mouse=self.control.mouse)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.background, (0, 0))
        self.button.draw(surface=surface)
