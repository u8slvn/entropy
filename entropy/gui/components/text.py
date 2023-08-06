from __future__ import annotations

import pygame
import pygame as pg

from entropy import translator
from entropy.utils import Pos


T = translator


class Text:
    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        color: pg.Color | str,
        background: pg.Color | str | None = None,
    ) -> None:
        self.__text = text
        self._text = T(self.__text)
        self._font = font
        self._color = color
        self._background = background
        self._surface, self._rect = self._render()
        self._pos: Pos | None = None
        self._center_pos: Pos | None = None
        translator.register(subject=self)

    @property
    def width(self) -> int:
        return self._rect.width

    @property
    def height(self) -> int:
        return self._rect.height

    def set_center_pos(self, pos: Pos) -> None:
        self._rect.center = pos
        self._center_pos = pos

    def set_pos(self, pos: Pos) -> None:
        self._rect.topleft = pos
        self._pos = pos

    def _render(self) -> tuple[pg.Surface, pg.Rect]:
        surface = self._font.render(self._text, True, self._color, self._background)
        rect = surface.get_rect()

        return surface, rect

    def update(self) -> None:
        self._text = T(self.__text)
        self._surface, self._rect = self._render()
        if self._center_pos is not None:
            self.set_center_pos(pos=self._center_pos)
        elif self._pos is not None:
            self.set_pos(pos=self._pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._rect)
