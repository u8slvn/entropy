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
        self.text = text
        self.color = color
        self.font = font
        self.background = background
        self.surf = self._render()

        rect = pygame.Rect(*(pos + parent.pos), *self.surf.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

    def _render(self) -> pygame.Surface:
        return self.font.render(self.text, False, self.color, self.background)

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, self.rect)

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
        self.locale_changed = False

        super().__init__(
            parent=parent,
            text=T(text),
            color=color,
            font=font,
            background=background,
            pos=pos,
            align=align,
        )

        self.surf = self._render()

    def on_notify(self) -> None:
        self.locale_changed = True

    def setup(self) -> None:
        super().setup()
        translator.add_observer(observer=self)

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        if self.locale_changed is True:
            self.locale_changed = False
            self.text = T(self.__text)
            self.surf = self._render()

            rect = pygame.Rect(*self.pos, *self.surf.get_size())
            self.rect = rect
            self.update_align()

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.surf, self.rect)

    def teardown(self) -> None:
        translator.remove_observer(observer=self)

    def __repr__(self):
        return f'<TText value="{self.__text}">'
