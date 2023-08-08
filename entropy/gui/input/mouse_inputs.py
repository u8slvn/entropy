from __future__ import annotations

from math import ceil

import pygame

import entropy

from entropy.gui.input import InputsBase
from entropy.utils import Pos


class MouseInputs(InputsBase):
    def __init__(self) -> None:
        self.BUTTON1 = False
        self.BUTTON2 = False
        self.BUTTON3 = False
        self._pos = Pos(0, 0)

    def parse_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.pos = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.BUTTON1 = True
            elif event.button == 2:
                self.BUTTON2 = True
            elif event.button == 2:
                self.BUTTON3 = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.BUTTON1 = False
            elif event.button == 2:
                self.BUTTON2 = False
            elif event.button == 2:
                self.BUTTON3 = False

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

    def reset(self) -> None:
        self.BUTTON1 = False
        self.BUTTON2 = False
        self.BUTTON3 = False
        # Never reset self._pos as we want to always know where the mouse is.
