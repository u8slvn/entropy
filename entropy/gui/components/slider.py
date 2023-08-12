from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import assets
from entropy import mixer
from entropy import mouse
from entropy.constants import GUI_TEXT_COLOR
from entropy.constants import SLIDER_BG_COLOR
from entropy.constants import SLIDER_PROGRESS_COLOR
from entropy.gui.components.text import Text
from entropy.gui.components.widget import WidgetComponent
from entropy.mixer import Channel
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.input import Inputs
    from entropy.utils import Size


class Slider(WidgetComponent):
    def __init__(
        self,
        pos: Pos,
        size: Size,
        min: int,
        max: int,
        button: pygame.Surface,
        initial_value: float,
        channel: Channel,
    ) -> None:
        self._pos = pos
        self._size = size
        self._min = min
        self._max = max
        self._channel = channel
        self._focus = False
        self._grabbed = False
        self._min_pos = self._pos.x
        self._max_pos = self._pos.x + self._size.w
        self._background = pygame.Rect(*self._pos, *self._size)
        self._progress = pygame.Rect(*self._pos, *self._size)
        self._buttons = self._build_buttons(button)
        self._button = self._buttons[self._focus]
        self._button_rect = self._button.get_rect()
        self._button_rect.topleft = (
            self._pos.x,
            self._pos.y - (self._button_rect.h - self._size.h) // 2,
        )
        self._button_x = 0
        self.set_value(initial_value)
        self._last_value = self.get_value()

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

    @property
    def width(self) -> int:
        return self._size.w

    @property
    def height(self) -> int:
        return self._button_rect.h

    def set_focus(self) -> None:
        self._focus = True

    def unset_focus(self) -> None:
        self._focus = False

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

        value = (button_value / self.range_value) * (self._max - self._min) + self._min
        return round(value, 2)

    def set_value(self, value: float) -> None:
        self._button_x = int(self._min_pos + self.range_value * value)

    def setup(self) -> None:
        self.move_slider(x=self._button_x)

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.collide_with(self._background) or mouse.collide_with(
            self._button_rect
        ):
            if mouse.is_button_pressed(mouse.BUTTON1):
                self._grabbed = True
        if not mouse.is_button_pressed(mouse.BUTTON1):
            self._grabbed = False
        if mouse.collide_with(self._button_rect) or self._grabbed:
            self._focus = True
        else:
            self._focus = False

        if self._grabbed:
            self._button_x = mouse.pos.x

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
    _margin = 15

    def __init__(
        self,
        text: str,
        pos: Pos,
        size: Size,
        min: int,
        max: int,
        button: pygame.Surface,
        initial_value: float,
        channel: Channel,
    ) -> None:
        font = assets.fonts.get("LanaPixel", "small")
        self._text = Text(text=text, font=font, color=GUI_TEXT_COLOR)
        slider_pos = Pos(pos.x, pos.y + self._text.height + self._margin)
        self._text.set_pos(Pos(pos.x + ((size.w - self._text.width) // 2), pos.y))
        super().__init__(
            pos=slider_pos,
            size=size,
            min=min,
            max=max,
            button=button,
            initial_value=initial_value,
            channel=channel,
        )

    @property
    def height(self) -> int:
        return super().height + self._margin + self._text.height

    def setup(self) -> None:
        self._text.setup()
        super().setup()

    def update(self) -> None:
        self._text.update()
        super().update()

    def draw(self, surface: pygame.Surface) -> None:
        self._text.draw(surface=surface)
        super().draw(surface=surface)
