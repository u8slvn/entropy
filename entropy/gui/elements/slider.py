from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable

import pygame as pg

from entropy import mixer
from entropy import mouse
from entropy.constants import SLIDER_BG_COLOR
from entropy.constants import SLIDER_PROGRESS_COLOR
from entropy.event.specs import click_is_pressed
from entropy.event.specs import click_is_released
from entropy.event.specs import left_or_right_is_pressed
from entropy.event.types import inputs
from entropy.gui.elements.base import UIElement
from entropy.gui.elements.text import Text
from entropy.utils.measure import Size


if TYPE_CHECKING:
    from entropy.event.event import Event


class Slider(UIElement):
    _step = 0.1
    _text_margin = 12

    def __init__(
        self,
        *groups: Any,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        update_callback: Callable[[float], None],
        button_image: pg.Surface,
        sound_focus: str,
        sound_on_hold: Callable[[], None] | None = None,
        text: str | None = None,
        text_color: pg.Color | None = None,
        text_font: pg.font.Font | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*groups)
        self._focus = False
        self._grabbed = False
        self._last_value = 0.0
        self._value = initial_value
        self._min_value = min_value
        self._max_value = max_value
        self._sound_focus = sound_focus
        self._sound_on_hold = sound_on_hold
        self._update_callback = update_callback
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect(**kwargs)
        self._progress = self.rect.copy()
        self._button = _SliderButton(
            image=button_image, focus=self._focus, center=self.rect.center
        )
        self.set_value(value=self._value)
        if all([text, text_color, text_font]):
            self.text = Text(
                *groups,
                text=text,
                color=text_color,
                font=text_font,
            )
            self.text.move(
                center=(
                    self.rect.centerx,
                    self.rect.top - self._text_margin - self.text.rect.h // 2,
                )
            )
        else:
            self.text = None

    @property
    def min(self) -> int:
        return self.rect.left

    @property
    def max(self) -> int:
        return self.rect.right

    @property
    def range(self) -> int:
        return self.max - self.min

    def move(self, **kwargs: Any) -> None:
        self.rect = self.image.get_rect(**kwargs)
        self._progress.topleft = self.rect.topleft
        self._button.move(center=self.rect.center)
        if self.text is not None:
            self.text.move(
                center=(
                    self.rect.centerx,
                    self.rect.top - self._text_margin - self.text.rect.h // 2,
                )
            )
        self.set_value(value=self._value)

    def set_focus(self) -> None:
        if self._focus:
            return

        self._focus = True
        self._button.focus = True
        mixer.play_uisfx(self._sound_focus)

    def unset_focus(self) -> None:
        self._focus = False
        self._button.focus = False

    def has_focus(self) -> bool:
        return self._focus

    def move_slider(self, value: int) -> None:
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max

        self._button.value = value
        self._progress.w = value - self.min

    def get_value(self) -> float:
        button_value = self._button.value - self.min
        value = (button_value / self.range) * (
            self._max_value - self._min_value
        ) + self._min_value
        return round(value, 2)

    def set_value(self, value: float) -> None:
        self._last_value = self.get_value()
        value = self.min + self.range * value
        self.move_slider(value=int(value))

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        if mouse.visible:
            bar_collide = mouse.collide_with(self.rect)
            button_collide = mouse.collide_with(self._button.rect)

            if (bar_collide or button_collide) and click_is_pressed(event):
                self._grabbed = True

            if button_collide or self._grabbed:
                self.set_focus()
            else:
                self.unset_focus()

            if self._grabbed:
                if click_is_released(event):
                    self._grabbed = False
                else:
                    self._button.value = min(max(mouse.pos.x, self.min), self.max)

        elif self.has_focus():
            if left_or_right_is_pressed(event):
                value = round(self.get_value(), 1)
                if event.key == inputs.LEFT:
                    self.set_value(value - self._step)
                else:
                    self.set_value(value + self._step)

                self._grabbed = True
            else:
                self._grabbed = False

    def update(self, dt: float) -> None:
        self._button.update()
        if self._grabbed:
            self.move_slider(self._button.value)

            if self._sound_on_hold is not None:
                self._sound_on_hold()

            value = self.get_value()
            if self._last_value != value:
                self._update_callback(value)

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, SLIDER_BG_COLOR, self.rect)
        pg.draw.rect(surface, SLIDER_PROGRESS_COLOR, self._progress)
        self._button.draw(surface)


class _SliderButton:
    def __init__(self, image: pg.Surface, focus: bool, **kwargs: Any) -> None:
        self.focus = focus
        self._images = self._build_images(image)
        self._image = self._images[self.focus]
        self.rect = self._image.get_rect(**kwargs)

    @staticmethod
    def _build_images(image: pg.Surface) -> list[pg.Surface]:
        width = image.get_width()
        height = image.get_height() // 2

        x = y = 0
        buttons = []
        for btn in range(2):
            buttons.append(image.subsurface((x, y, width, height)))
            y += height

        return buttons

    @property
    def value(self) -> int:
        return self.rect.centerx

    @value.setter
    def value(self, value: int) -> None:
        self.rect.centerx = value

    @property
    def size(self) -> Size:
        return Size(*self._image.get_size())

    def move(self, **kwargs: Any) -> None:
        self.rect = self._image.get_rect(**kwargs)

    def update(self) -> None:
        self._image = self._images[self.focus]

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._image, self.rect)
