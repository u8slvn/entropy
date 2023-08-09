from __future__ import annotations

from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from entropy.gui.input import Inputs


class Mouse:
    BUTTON1 = 0
    BUTTON2 = 1
    BUTTON3 = 2

    def __init__(self) -> None:
        self.__nb_moves = 0
        self.__nb_moves_before_show = 2

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            self.hide()

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

    @staticmethod
    def is_visible() -> bool:
        return pygame.mouse.get_visible()
