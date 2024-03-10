from __future__ import annotations

from typing import Any

import pygame as pg

from entropy.gui.component.base import Sprite


class Text(Sprite):
    def __init__(
        self,
        *groups: Any,
        text: str,
        color: pg.Color,
        font: pg.font.Font,
        bgcolor: pg.Color | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*groups)
        self._text = text
        self._color = color
        self._font = font
        self._bgcolor = bgcolor
        self.image = self._render()
        self.rect = self.image.get_rect(**kwargs)

    def _render(self) -> pg.Surface:
        return self._font.render(self._text, False, self._color, self._bgcolor)
