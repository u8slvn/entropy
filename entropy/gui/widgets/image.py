from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import assets
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.base import Widget
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.event.event import Event


class Image(Widget):
    def __init__(
        self,
        parent: Widget,
        name: str,
        pos: Pos = Pos(0, 0),
        align: Align | None = None,
    ) -> None:
        self._surf = assets.image.get(name=name)
        rect = pygame.Rect(*pos, *self._surf.get_size())
        super().__init__(parent=parent, rect=rect, align=align)

    def set_alpha(self, value: int) -> None:
        self._surf.set_alpha(value)

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.pos)

    def teardown(self) -> None:
        pass
