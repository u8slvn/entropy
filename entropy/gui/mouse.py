from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

import pygame as pg

import entropy

from entropy.event.types import inputs
from entropy.event.types import system
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event


class Mouse:
    def __init__(self) -> None:
        self._nb_moves = 0
        self._nb_moves_before_show = 2
        self._pos: Pos = Pos(0, 0)
        self.visible = True

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

    def process_event(self, event: Event) -> None:
        if event.triggered and event.key == inputs.MOVE:
            self.pos = event.value
            self.visible = True
        elif event.triggered and event.key == system.HIDE_MOUSE:
            self.visible = False

    def update(self) -> None:
        if self.visible is True:
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

    def collide_with(self, rect: pg.Rect) -> bool:
        return rect.collidepoint(self.pos)
