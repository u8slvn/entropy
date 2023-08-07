from __future__ import annotations

from math import ceil

import pygame as pg

import entropy

from entropy.utils import Pos


class Mouse:
    def __init__(self) -> None:
        self.__nb_moves = 0
        self.__nb_moves_before_show = 2
        self.pos = Pos(*pg.mouse.get_pos())

    @staticmethod
    def _get_scale_mouse_position() -> Pos:
        """Get the mouse position scaled to the render screen."""
        mouse_pos = Pos(*pg.mouse.get_pos()) - entropy.window.render_margin
        return Pos(
            x=ceil(mouse_pos.x * entropy.window.render_scale.x),
            y=ceil(mouse_pos.y * entropy.window.render_scale.y),
        )

    def update(self) -> None:
        self.pos = self._get_scale_mouse_position()

        if pg.mouse.get_visible() is False:
            if pg.mouse.get_rel() != (0, 0):
                self.__nb_moves += 1
            else:
                self.__nb_moves = 0

            if self.__nb_moves > self.__nb_moves_before_show:
                self.__nb_moves = 0
                pg.mouse.set_visible(True)

    @staticmethod
    def is_visible() -> bool:
        return pg.mouse.get_visible()

    def hide(self) -> None:
        if self.is_visible():
            pg.mouse.set_visible(False)
