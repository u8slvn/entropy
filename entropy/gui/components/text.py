from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import translator
from entropy.game.entity import GameEntity
from entropy.gui.components.base import Component
from entropy.gui.components.base import UIComponent
from entropy.tools.observer import Observer
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.base import ALIGN
    from entropy.gui.input import Inputs

T = translator


class Text(UIComponent):
    def __init__(
        self,
        parent: Component | None,
        text: str,
        font: pygame.font.Font,
        color: Color | str,
        align: ALIGN | None = None,
        background: Color | str | None = None,
    ):
        super().__init__(parent=parent)
        self._text = text
        self._font = font
        self._color = color
        self.align = align
        self._background = background
        self._surf = self._render()
        self.set_rect(self._surf.get_rect())

    def _render(self) -> pygame.Surface:
        return self._font.render(self._text, False, self._color, self._background)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.pos)

    def teardown(self) -> None:
        pass


class TText(GameEntity, Observer):
    """Translated Text."""

    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: Color | str,
        background: Color | str | None = None,
    ) -> None:
        self.__text = text
        self._text = T(self.__text)
        self._font = font
        self._color = color
        self._background = background
        self._surface, self._rect = self._render()
        self._pos: Pos | None = None
        self._center_pos: Pos | None = None
        self._locale_changed = False

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

    def _render(self) -> tuple[pygame.Surface, pygame.Rect]:
        surface = self._font.render(self._text, True, self._color, self._background)
        rect = surface.get_rect()

        return surface, rect

    def on_notify(self) -> None:
        self._locale_changed = True

    def setup(self) -> None:
        translator.add_observer(observer=self)

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        if self._locale_changed is True:
            self._locale_changed = False
            self._text = T(self.__text)
            self._surface, self._rect = self._render()
            if self._center_pos is not None:
                self.set_center_pos(pos=self._center_pos)
            elif self._pos is not None:
                self.set_pos(pos=self._pos)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, self._rect)

    def teardown(self) -> None:
        translator.remove_observer(observer=self)

    def __repr__(self):
        return f'<Text value="{self.__text}">'
