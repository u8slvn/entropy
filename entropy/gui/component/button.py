from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame as pg

from entropy import mixer
from entropy import mouse
from entropy.event.specs import b_is_pressed
from entropy.event.specs import b_or_click_is_pressed
from entropy.gui.component.base import Sprite
from entropy.gui.component.text import Text


if TYPE_CHECKING:
    from entropy.event.event import Event


class _ButtonState(IntEnum):
    NORMAL = 0
    FOCUS = 1
    CHECKED = 2
    FOCUS_CHECKED = 3


class Button(Sprite):
    def __init__(
        self,
        *groups: Any,
        image: pg.Surface,
        text: str | None = None,
        text_color: pg.Color | None = None,
        text_font: pg.font.Font | None = None,
        focus_sound: str,
        click_sound: str,
        action: Callable[[], None],
        checked: bool = False,
        **kwargs,
    ):
        super().__init__(*groups)
        self._baseimage = image
        self._images = self._build_images()
        self._text = text
        self._text_color = text_color
        self._text_font = text_font
        self._focus_sound = focus_sound
        self._click_sound = click_sound
        self._action = action
        self._state = _ButtonState.CHECKED if checked else _ButtonState.NORMAL
        self._pressed = False
        self.image = self._images[self._state]
        self.rect = self.image.get_rect(**kwargs)
        self.text = Text(
            *groups,
            text=text,
            color=text_color,
            font=text_font,
            center=self.rect.center,
        )

    def _build_images(self) -> dict[_ButtonState, pg.Surface]:

        width = self._baseimage.get_width()
        height = self._baseimage.get_height() // 4

        x = y = 0
        images = {}
        for btn_state in _ButtonState:
            images[btn_state] = self._baseimage.subsurface((x, y, width, height))
            y += height

        return images

    def _render_text(self) -> pg.Surface:
        return self._text_font.render(self._text, False, self._text_color)

    def check(self) -> None:
        if self.has_focus():
            self._state = _ButtonState.FOCUS_CHECKED
        else:
            self._state = _ButtonState.CHECKED

    def uncheck(self) -> None:
        if self.has_focus():
            self._state = _ButtonState.FOCUS
        else:
            self._state = _ButtonState.NORMAL

    def is_checked(self) -> bool:
        return self._state in [_ButtonState.CHECKED, _ButtonState.FOCUS_CHECKED]

    def set_focus(self) -> None:
        if self.is_checked():
            self._state = _ButtonState.FOCUS_CHECKED
        else:
            self._state = _ButtonState.FOCUS
        mixer.play_uisfx(self._focus_sound)

    def unset_focus(self) -> None:
        if self.is_checked():
            self._state = _ButtonState.CHECKED
        else:
            self._state = _ButtonState.NORMAL

    def has_focus(self) -> bool:
        return self._state in [_ButtonState.FOCUS, _ButtonState.FOCUS_CHECKED]

    def press(self) -> None:
        self._pressed = True

    def release(self) -> None:
        self._pressed = False
        mixer.play_uisfx(self._click_sound)
        self._action()

    def is_pressed(self) -> bool:
        return self._pressed

    def process_event(self, event: Event) -> None:
        if mouse.visible:
            if mouse.collide_with(self.rect):
                if not self.has_focus():
                    self.set_focus()
                if b_or_click_is_pressed(event):
                    self.press()
            else:
                self.unset_focus()
        elif b_is_pressed(event) and self.has_focus():
            self.press()

    def update(self, dt: float) -> None:
        if self.is_pressed():
            self.release()
        self.image = self._images[self._state]
