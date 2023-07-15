from __future__ import annotations

from math import ceil

import pygame as pg

import entropy

from entropy.utils import Pos


class Mouse:
    _nb_moves_before_show = 2

    def __init__(self) -> None:
        self._nb_moves = 0
        self._last_pos = Pos(0, 0)
        self.pos = Pos(*pg.mouse.get_pos())

    def update(self) -> None:
        mouse_pos = Pos(*pg.mouse.get_pos())
        self.pos = Pos(
            x=ceil(mouse_pos.x * entropy.window.render_scale.x),
            y=ceil(mouse_pos.y * entropy.window.render_scale.y),
        )

        if pg.mouse.get_visible() is False:
            if pg.mouse.get_rel() != (0, 0):
                self._nb_moves += 1
            else:
                self._nb_moves = 0

            if self._nb_moves > self._nb_moves_before_show:
                self._nb_moves = 0
                pg.mouse.set_visible(True)
                pg.mouse.set_pos(self._last_pos)

    def hide(self) -> None:
        if pg.mouse.get_visible() is True:
            self._last_pos = self.pos
            pg.mouse.set_visible(False)
