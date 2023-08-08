from __future__ import annotations

from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from entropy.gui.input import Inputs


class Mouse:
    def __init__(self) -> None:
        self.__nb_moves = 0
        self.__nb_moves_before_show = 2

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.KEYUP or inputs.keyboard.KEYDOWN:
            self.hide()

    def update(self) -> None:
        if pygame.mouse.get_visible() is False:
            if pygame.mouse.get_rel() != (0, 0):
                self.__nb_moves += 1
            else:
                self.__nb_moves = 0

            if self.__nb_moves > self.__nb_moves_before_show:
                self.__nb_moves = 0
                pygame.mouse.set_visible(True)

    @staticmethod
    def is_visible() -> bool:
        return pygame.mouse.get_visible()

    def hide(self) -> None:
        if self.is_visible():
            pygame.mouse.set_visible(False)
