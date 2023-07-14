from __future__ import annotations

from math import ceil

import pygame as pg

from entropy.misc.window import Window
from entropy.utils import Pos


class Mouse:
    def __init__(self, window: Window):
        self.pos = Pos(*pg.mouse.get_pos())
        self.window = window

    def update_pos(self):
        mouse_pos = Pos(*pg.mouse.get_pos())
        self.pos = Pos(
            x=ceil(mouse_pos.x * self.window.render_scale.x),
            y=ceil(mouse_pos.y * self.window.render_scale.y),
        )
