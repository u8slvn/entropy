from __future__ import annotations

from typing import Callable

import pygame as pg

from entropy.components.text import Text
from entropy.misc.mouse import Mouse
from entropy.utils import Pos


class Button:
    def __init__(
        self,
        image: pg.Surface,
        image_hover: pg.Surface,
        sound_hover: pg.mixer.Sound,
        sound_clicked: pg.mixer.Sound,
        onclick: Callable[[], None],
        pos: Pos,
    ) -> None:
        super().__init__()
        self.hover = False
        self.pressed = False
        self.images = [image, image_hover]
        self.image = self.images[self.hover]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.sound_hover = sound_hover
        self.sound_clicked = sound_clicked
        self.onclick = onclick

    def update(self, mouse: Mouse) -> None:
        if hover := self.rect.collidepoint(mouse.pos):
            if not self.hover:
                self.sound_hover.play()

            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed is True:
                self.sound_clicked.play()
                self.pressed = False
                self.onclick()

        self.hover = hover
        self.image = self.images[self.hover]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)


class TextButton(Button):
    def __init__(
        self,
        text: Text,
        text_hover: Text,
        image: pg.Surface,
        image_hover: pg.Surface,
        sound_hover: pg.mixer.Sound,
        sound_clicked: pg.mixer.Sound,
        onclick: Callable[[], None],
        pos: Pos,
    ) -> None:
        super().__init__(
            image=image,
            image_hover=image_hover,
            sound_hover=sound_hover,
            sound_clicked=sound_clicked,
            onclick=onclick,
            pos=pos,
        )
        text.set_center_pos(Pos(*self.rect.center))
        text_hover.set_center_pos(Pos(*self.rect.center))
        self.texts = [text, text_hover]
        self.text = self.texts[self.hover]

    def update(self, mouse: Mouse) -> None:
        super().update(mouse=mouse)
        self.text = self.texts[self.hover]

    def draw(self, surface: pg.Surface) -> None:
        super().draw(surface=surface)
        surface.blit(self.text.surface, self.text.rect)
