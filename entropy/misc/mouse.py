from __future__ import annotations

from math import ceil

import pygame as pg

from entropy.misc.window import Window


class Mouse:
    def __init__(self, window: Window):
        self.pos = pg.mouse.get_pos()
        self.window = window

    def update_pos(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        scale_x, scale_y = self.window.render_scale
        self.pos = ceil(mouse_x * scale_x), ceil(mouse_y * scale_y)
