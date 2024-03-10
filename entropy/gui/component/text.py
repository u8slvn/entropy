from __future__ import annotations

import pygame as pg


class Text(pg.sprite.DirtySprite):
    def __init__(
        self,
        *groups: tuple[pg.sprite.Group, ...],
        text: str,
        color: pg.Color,
        font: pg.font.Font,
        center: tuple[int, int],
        bgcolor: pg.Color | None = None,
    ):
        super().__init__(*groups)
        self._text = text
        self._color = color
        self._font = font
        self._bgcolor = bgcolor
        self.image = self._render()
        self.rect = self.image.get_rect(center=center)

    def _render(self) -> pg.Surface:
        return self._font.render(self._text, False, self._color, self._bgcolor)
