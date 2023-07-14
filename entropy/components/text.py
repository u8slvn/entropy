from __future__ import annotations

import pygame as pg


class Text:
    def __init__(
        self,
        text: str,
        font: pg.font.Font,
        color: pg.Color | str,
        background: pg.Color | str | None = None,
    ):
        self.text = text
        self.font = font
        self.color = color
        self.background = background
        self.surface, self.rect = self._render()

    def _render(self) -> tuple[pg.Surface, pg.Rect]:
        surface = self.font.render(self.text, True, self.color, self.background)
        rect = surface.get_rect()
        return surface, rect

    def reload(self) -> None:
        self.surface, self.rect = self._render()
