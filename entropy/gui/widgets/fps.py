from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pygame

import entropy

from entropy.event.types import inputs
from entropy.game.entity import GameEntity
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event


class FPSViewer(GameEntity):
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

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        if event.pressed and event.key == inputs.DEBUG:
            self._visible = not self._visible

    def update(self, dt: float) -> None:
        if self._visible:
            self._fps = self._clock.get_fps()
            self._text = self._get_text()
            self._pos = self._get_pos()

    def draw(self, surface: pygame.Surface) -> None:
        if self._visible:
            surface.blit(self._text, self._pos)

    def teardown(self) -> None:
        pass
