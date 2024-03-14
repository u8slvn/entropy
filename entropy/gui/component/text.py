from __future__ import annotations

from typing import Any

import pygame as pg

from entropy import translator
from entropy.gui.component.base import Sprite
from entropy.tools.observer import Observer


T = translator


class Text(Sprite, Observer):
    def __init__(
        self,
        *groups: Any,
        text: str,
        color: pg.Color,
        font: pg.font.Font,
        bgcolor: pg.Color | None = None,
        translate: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(*groups)
        self._text = text
        self._color = color
        self._font = font
        self._bgcolor = bgcolor
        self._translated = translate
        self._locale_changed = False
        self._kwargs = kwargs
        self.image = self._render()
        self.rect = self.image.get_rect(**kwargs)
        if self._translated:
            translator.subscribe(observer=self)

    def _render(self) -> pg.Surface:
        text = T(self._text) if self._translated else self._text
        return self._font.render(text, False, self._color, self._bgcolor)

    def move(self, **kwargs: Any) -> None:
        super().move(**kwargs)
        self._kwargs = kwargs

    def on_notify(self) -> None:
        self._locale_changed = True

    def update(self, dt: float) -> None:
        if self._locale_changed is True:
            self._locale_changed = False
            self.image = self._render()
            self.rect = self.image.get_rect(**self._kwargs)

    def cleanup(self) -> None:
        if self._translated:
            translator.unsubscribe(observer=self)
