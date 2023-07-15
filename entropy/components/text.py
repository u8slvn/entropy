from __future__ import annotations

import pygame as pg

import entropy

from entropy.utils import Pos


_ = entropy.translator


class Text:
    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        color: pg.Color | str,
        background: pg.Color | str | None = None,
    ) -> None:
        self._text = text
        self.text = _(self._text)
        self.font = font
        self.color = color
        self.background = background
        self.surface, self.rect = self._render()
        self.center_pos = Pos(0, 0)
        entropy.translator.register_text(text=self)

    def set_center_pos(self, pos: Pos | None = None) -> None:
        if pos is not None:
            self.center_pos = pos
        self.rect.center = self.center_pos

    def _render(self) -> tuple[pg.Surface, pg.Rect]:
        surface = self.font.render(self.text, True, self.color, self.background)
        rect = surface.get_rect()

        return surface, rect

    def update(self) -> None:
        self.text = _(self._text)
        self.surface, self.rect = self._render()
        self.set_center_pos()
