from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import translator
from entropy.gui.components.base import Widget
from entropy.tools.observer import Observer
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.gui.components.base import ALIGN
    from entropy.gui.input import Inputs

T = translator


class Text(Widget):
    def __init__(
        self,
        parent: Widget,
        text: str,
        color: Color | str,
        font: pygame.font.Font,
        background: Color | str | None = None,
        pos: Pos = Pos(0, 0),
        align: ALIGN | None = None,
    ):
        self._text = text
        self._color = color
        self._font = font
        self._background = background
        self._surf = self._render()

        rect = pygame.Rect(*(pos + parent.pos), *self._surf.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

    def _render(self) -> pygame.Surface:
        return self._font.render(self._text, False, self._color, self._background)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect)

    def teardown(self) -> None:
        pass


class TText(Text, Observer):
    """Translated Text."""

    def __init__(
        self,
        parent: Widget,
        text: str,
        color: Color | str,
        font: pygame.font.Font,
        background: Color | str | None = None,
        pos: Pos = Pos(0, 0),
        align: ALIGN | None = None,
    ) -> None:
        self.__text = text
        self._locale_changed = False

        super().__init__(
            parent=parent,
            text=T(text),
            color=color,
            font=font,
            background=background,
            pos=pos,
            align=align,
        )

    def on_notify(self) -> None:
        self._locale_changed = True

    def setup(self) -> None:
        super().setup()
        translator.add_observer(observer=self)

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        if self._locale_changed is True:
            self._locale_changed = False
            self._text = T(self.__text)
            self._surf = self._render()

            rect = pygame.Rect(*self.pos, *self._surf.get_size())
            self.rect = rect
            self.update_align()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect)

    def teardown(self) -> None:
        translator.remove_observer(observer=self)

    def __repr__(self):
        return f'<TText value="{self.__text}">'
