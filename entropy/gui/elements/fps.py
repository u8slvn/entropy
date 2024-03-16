from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pygame

import entropy

from entropy.event.specs import debug_is_pressed
from entropy.gui.elements.base import UIElementBase
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event


class FPSViewer(UIElementBase):
    def __init__(self, clock: pygame.time.Clock) -> None:
        self._clock = clock
        self._fps = 60.0
        self._visible = False
        self._format = "{fps} FPS"
        self._font = pygame.font.SysFont("Arial", 20)
        self._text = self._get_text()
        self._pos = self._get_pos()

    def _get_text(self) -> pygame.Surface:
        text = self._format.format(fps=round(self._fps))
        return self._font.render(text, True, "white")

    def _get_pos(self) -> Pos:
        return Pos(
            entropy.window.default_res.w - self._text.get_width(),
            entropy.window.default_res.h - self._text.get_height(),
        )

    def process_event(self, event: Event) -> None:
        if debug_is_pressed(event):
            self._visible = not self._visible

    def update(self, dt: float) -> None:
        if self._visible:
            self._fps = self._clock.get_fps()
            self._text = self._get_text()
            self._pos = self._get_pos()

    def draw(self, surface: pygame.Surface) -> None:
        if self._visible:
            surface.blit(self._text, self._pos)
