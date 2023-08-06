from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame
import pygame as pg

from entropy import config
from entropy import mouse
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.text import Text
    from entropy.tools.observer import Observer


class ButtonState(IntEnum):
    NORMAL = 0
    FOCUS = 1
    CHECKED = 2
    FOCUS_CHECKED = 3


class Button:
    def __init__(
        self,
        text: Text,
        image: pg.Surface,
        sound_focus: pg.mixer.Sound,
        sound_clicked: pg.mixer.Sound,
        callback: Callable[[], None],
        pos: Pos,
        padding: Pos = Pos(0, 0),
    ) -> None:
        super().__init__()
        self._pressed = False
        self._images = self._build_images(image=image)
        self._image = self._images[ButtonState.NORMAL]
        self._rect = self._image.get_rect()
        self._rect.topleft = pos
        self._state = ButtonState.NORMAL

        x, y = self._rect.center
        text.set_center_pos(Pos(x + padding.x, y + padding.y))
        self._text = text

        self._sound_focus = sound_focus
        self._sound_clicked = sound_clicked

        self._callback = callback

    @staticmethod
    def _build_images(image: pygame.Surface) -> dict[int, pygame.Surface]:
        width = image.get_width()
        height = image.get_height() / 4

        x = y = 0
        images = {}
        for btn_state in ButtonState:
            images[btn_state] = image.subsurface((x, y, width, height))
            y += height

        return images

    def collide_mouse(self) -> bool:
        return self._rect.collidepoint(mouse.pos)

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False
        self.click()

    def is_pressed(self) -> bool:
        return self._pressed

    def check(self) -> None:
        if self.has_focus():
            self._state = ButtonState.FOCUS_CHECKED
        else:
            self._state = ButtonState.CHECKED

    def uncheck(self) -> None:
        if self.has_focus():
            self._state = ButtonState.FOCUS
        else:
            self._state = ButtonState.NORMAL

    def is_checked(self) -> bool:
        return self._state in [ButtonState.CHECKED, ButtonState.FOCUS_CHECKED]

    def set_focus(self):
        if self.is_checked():
            self._state = ButtonState.FOCUS_CHECKED
        else:
            self._state = ButtonState.FOCUS
        self._sound_focus.play()

    def unset_focus(self):
        if self.is_checked():
            self._state = ButtonState.CHECKED
        else:
            self._state = ButtonState.NORMAL

    def has_focus(self) -> bool:
        return self._state in [ButtonState.FOCUS, ButtonState.FOCUS_CHECKED]

    def click(self) -> None:
        self._sound_clicked.play()
        self._callback()

    def update(self):
        self._image = self._images[self._state]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._image, self._rect)
        surface.blit(self._text.surface, self._text.rect)


class ObservableButton(Button):
    _observer: Observer

    def __init__(self, *args, watch: str, match: Any, **kwargs):
        super().__init__(*args, **kwargs)
        self._watch = watch
        self._match = match
        self._observer.register(subject=self)

    def update(self):
        if getattr(self._observer, self._watch) == self._match:
            self.check()
        else:
            self.uncheck()
        super().update()


class ConfigObservableButton(ObservableButton):
    _observer = config
