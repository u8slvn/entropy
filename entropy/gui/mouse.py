from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.input import Inputs


class Mouse:
    BUTTON1 = 0
    BUTTON2 = 1
    BUTTON3 = 2

    def __init__(self) -> None:
        self.__nb_moves = 0
        self.__nb_moves_before_show = 2
        self._pos: Pos = Pos(0, 0)

    @property
    def pos(self) -> Pos:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        mouse_pos = Pos(*pos) - entropy.window.render_margin
        self._pos = Pos(
            x=ceil(mouse_pos.x * entropy.window.render_scale.x),
            y=ceil(mouse_pos.y * entropy.window.render_scale.y),
        )

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            self.hide()

        if inputs.mouse.POS is not None:
            self.pos = inputs.mouse.POS

    def update(self) -> None:
        if self.is_visible() is False:
            if pygame.mouse.get_rel() != (0, 0):
                self.__nb_moves += 1
            else:
                self.__nb_moves = 0

            if self.__nb_moves > self.__nb_moves_before_show:
                self.__nb_moves = 0
                self.show()

    def is_button_pressed(self, __button: int) -> bool:
        assert self.BUTTON1 <= __button <= self.BUTTON3
        return pygame.mouse.get_pressed()[__button]

    def show(self) -> None:
        if not self.is_visible():
            pygame.mouse.set_visible(True)

    def hide(self) -> None:
        if self.is_visible():
            pygame.mouse.set_visible(False)

    def collide_with(self, __rect: pygame.Rect) -> bool:
        return __rect.collidepoint(self.pos)

    @staticmethod
    def is_visible() -> bool:
        return pygame.mouse.get_visible()
