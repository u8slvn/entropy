from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import mouse
from entropy.game.entity import GameEntity


if TYPE_CHECKING:
    from entropy.gui.input import Inputs
    from entropy.utils import Pos
    from entropy.utils import Size

UNSELECTED = "red"
SELECTED = "white"

BUTTONSTATES = {True: SELECTED, False: UNSELECTED}


class Slider(GameEntity):
    def __init__(
        self, pos: Pos, size: Size, min: int, max: int, initial_value: float
    ) -> None:
        self._pos = pos
        self._size = size
        self._min = min
        self._max = max
        self._focus = False
        self._grabbed = False
        self._value_changed = False
        self._min_pos = self._pos.x - (self._size.w // 2)
        self._max_pos = self._pos.x + (self._size.w // 2)
        self._top_pos = self._pos.y - (self._size.h // 2)
        self._container = pygame.Rect(self._min_pos, self._top_pos, *self._size)
        self._cursor = pygame.Rect(self._min_pos, self._top_pos, 10, self._size.h)
        self._cursor_x = 0
        self.value = initial_value

    @property
    def range_value(self) -> int:
        return self._max_pos - self._min_pos

    def move_slider(self, x: int) -> None:
        if x < self._min_pos:
            x = self._min_pos
        if x > self._max_pos:
            x = self._max_pos
        self._cursor.centerx = x

    @property
    def value(self) -> float:
        button_value = self._cursor.centerx - self._min_pos
        value = (button_value / self.range_value) * (self._max - self._min) + self._min
        return round(value, 1)

    @value.setter
    def value(self, value: float) -> None:
        self._cursor_x = int(self._min_pos + self.range_value * value)

    def setup(self) -> None:
        self.move_slider(x=self._cursor_x)

    def process_inputs(self, inputs: Inputs) -> None:
        if mouse.collide_with(self._container):
            if mouse.is_button_pressed(mouse.BUTTON1):
                self._grabbed = True
        if not mouse.is_button_pressed(mouse.BUTTON1):
            self._grabbed = False
        if mouse.collide_with(self._cursor):
            self._focus = True

        if self._grabbed:
            self._cursor_x = mouse.pos.x
        else:
            self._focus = False

    def update(self) -> None:
        if self._grabbed:
            self.move_slider(self._cursor_x)

        if self._value_changed:
            self._value_changed = False
            print("Save")

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "black", self._container)
        pygame.draw.rect(surface, BUTTONSTATES[self._focus], self._cursor)

    def teardown(self) -> None:
        pass
