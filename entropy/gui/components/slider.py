from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import mixer
from entropy import mouse
from entropy.constants import SLIDER_BG_COLOR
from entropy.constants import SLIDER_PROGRESS_COLOR
from entropy.gui.components.text import TText
from entropy.gui.components.widget import WidgetComponent
from entropy.mixer import Channel
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.input import Inputs
    from entropy.utils import Size


class Slider(WidgetComponent):
    _step = 0.1

    def __init__(
        self,
        pos: Pos,
        size: Size,
        min_value: int,
        max_value: int,
        button: pygame.Surface,
        initial_value: float,
        sound_focus: str,
        channel: Channel,
    ) -> None:
        self._pos = pos
        self._size = size
        self._min_value = min_value
        self._max_value = max_value
        self._sound_focus = sound_focus
        self._channel = channel
        self._focus = False
        self._grabbed = False
        self._min_pos = 0
        self._max_pos = 0
        self._background = pygame.Rect(*self._pos, *self._size)
        self._progress = pygame.Rect(*self._pos, *self._size)
        self._buttons = self._build_buttons(button)
        self._button = self._buttons[self._focus]
        self._button_rect = self._button.get_rect()
        self._button_x = 0
        self._last_value = 0
        self._initial_value = initial_value
        self._setup_pos()

    def _setup_pos(self) -> None:
        self._min_pos = self._pos.x
        self._max_pos = self._pos.x + self._size.w
        self._background.topleft = self._pos
        self._progress.topleft = self._pos
        self._button_rect.topleft = (
            self._pos.x,
            self._pos.y - (self._button_rect.h - self._size.h) // 2,
        )
        self.set_value(value=self._initial_value)

    @staticmethod
    def _build_buttons(image: pygame.Surface) -> list[pygame.Surface]:
        width = image.get_width()
        height = image.get_height() // 2

        x = y = 0
        buttons = []
        for btn in range(2):
            buttons.append(image.subsurface((x, y, width, height)))
            y += height

        return buttons

    def get_width(self) -> int:
        return self._size.w

    def get_height(self) -> int:
        return self._button_rect.h

    def set_pos(self, pos: Pos) -> None:
        self._pos = pos
        self._setup_pos()

    def set_focus(self) -> None:
        if self.has_focus():
            return

        self._focus = True
        mixer.play_uisfx(self._sound_focus)

    def unset_focus(self) -> None:
        self._focus = False

    def has_focus(self) -> None:
        return self._focus is True

    @property
    def range_value(self) -> int:
        return self._max_pos - self._min_pos

    def move_slider(self, x: int) -> None:
        if x < self._min_pos:
            x = self._min_pos
        if x > self._max_pos:
            x = self._max_pos
        self._button_rect.centerx = x
        self._progress.w = self._button_rect.centerx - self._min_pos

    def get_value(self) -> float:
        button_value = self._button_rect.centerx - self._min_pos

        value = (button_value / self.range_value) * (
            self._max_value - self._min_value
        ) + self._min_value
        return round(value, 2)

    def set_value(self, value: float) -> None:
        self._last_value = self.get_value()
        self._button_x = int(self._min_pos + self.range_value * value)
        self.move_slider(x=self._button_x)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.is_visible():
            if mouse.collide_with(self._background) or mouse.collide_with(
                self._button_rect
            ):
                if inputs.mouse.BUTTON1 and mouse.is_button_pressed(mouse.BUTTON1):
                    self._grabbed = True
            if not mouse.is_button_pressed(mouse.BUTTON1):
                self._grabbed = False
            if mouse.collide_with(self._button_rect) or self._grabbed:
                self.set_focus()
            else:
                self.unset_focus()

            if self._grabbed:
                self._button_x = mouse.pos.x

        elif self.has_focus():
            self._grabbed = True

            if inputs.keyboard.LEFT:
                value = round(self.get_value(), 1)
                self.set_value(value - self._step)
                mixer.play_uisfx(self._sound_focus)
            elif inputs.keyboard.RIGHT:
                value = round(self.get_value(), 1)
                self.set_value(value + self._step)
                mixer.play_uisfx(self._sound_focus)
            else:
                self._grabbed = False

    def update(self) -> None:
        self._button = self._buttons[self._focus]
        if self._grabbed:
            self.move_slider(self._button_x)

            value = self.get_value()
            if self._last_value != value:
                mixer.set_volume(value, self._channel)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, SLIDER_BG_COLOR, self._background)
        pygame.draw.rect(surface, SLIDER_PROGRESS_COLOR, self._progress)
        surface.blit(self._button, self._button_rect)

    def teardown(self) -> None:
        pass


class TitledSlider(Slider):
    _margin = 7

    def __init__(
        self,
        pos: Pos,
        text: TText,
        size: Size,
        min_value: int,
        max_value: int,
        initial_value: float,
        button: pygame.Surface,
        sound_focus: str,
        channel: Channel,
    ) -> None:
        super().__init__(
            pos=pos,
            size=size,
            min_value=min_value,
            max_value=max_value,
            initial_value=initial_value,
            button=button,
            sound_focus=sound_focus,
            channel=channel,
        )
        self._text = text
        self.set_pos(pos=pos)

    def get_height(self) -> int:
        return super().get_height() + self._margin + self._text.height

    def set_pos(self, pos: Pos) -> None:
        super().set_pos(
            pos=Pos(pos.x, pos.y + self._text.height + self._margin),
        )
        self._text.set_pos(
            pos=Pos(pos.x + ((self._size.w - self._text.width) // 2), pos.y),
        )

    def setup(self) -> None:
        super().setup()
        self._text.setup()

    def update(self) -> None:
        super().update()
        self._text.update()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface=surface)
        self._text.draw(surface=surface)
