from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Callable

import pygame as pg

from entropy import mouse
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.text import Text


class Button:
    def __init__(
        self,
        text: Text,
        text_focus: Text,
        image: pg.Surface,
        image_focus: pg.Surface,
        sound_focus: pg.mixer.Sound,
        sound_clicked: pg.mixer.Sound,
        callback: Callable[[], None],
        pos: Pos,
    ) -> None:
        super().__init__()
        self._focus = False
        self._pressed = False

        self._images = [image, image_focus]
        self._image = self._images[self._focus]
        self._rect = self._image.get_rect()
        self._rect.topleft = pos

        text.set_center_pos(Pos(*self._rect.center))
        text_focus.set_center_pos(Pos(*self._rect.center))
        self._texts = [text, text_focus]
        self._text = self._texts[self._focus]

        self._sound_selected = sound_focus
        self._sound_clicked = sound_clicked

        self._onclick = callback

    def collide_mouse(self) -> bool:
        return self._rect.collidepoint(mouse.pos)

    def is_pressed(self) -> bool:
        return self._pressed

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False
        self.click()

    def has_focus(self) -> bool:
        return self._focus

    def set_focus(self):
        self._focus = True
        self.update()
        self._sound_selected.play()

    def unset_focus(self):
        self._focus = False
        self.update()

    def click(self) -> None:
        self._sound_clicked.play()
        self._onclick()

    def update(self):
        self._text = self._texts[self._focus]
        self._image = self._images[self._focus]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._image, self._rect)
        surface.blit(self._text.surface, self._text.rect)
