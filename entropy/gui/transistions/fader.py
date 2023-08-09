from __future__ import annotations

from typing import Callable

import pygame

from entropy.gui.components.background import ColorBackground
from entropy.gui.transistions.base import Ease
from entropy.gui.transistions.base import Transition
from entropy.utils import Color


class _FaderTransition(Transition):
    def __init__(
        self,
        duration: int,
        callback: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(duration=duration, callback=callback)
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._alpha_rate = 255 / duration

    def _default_alpha_value(self) -> int:
        return 255 if self._ease is Ease.IN else 0

    def setup(self) -> None:
        super().setup()
        self._background.set_alpha(self._default_alpha_value())

    def update(self) -> None:
        super().update()

        if not self.is_active():
            return

        if self._ease is Ease.IN:
            alpha = max(int(self._timer.countdown * self._alpha_rate), 0)
        else:
            alpha = min(255 - int(self._timer.countdown * self._alpha_rate), 255)
        self._background.set_alpha(alpha)

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_active():
            surface.blit(self._background, self._background.pos)

    def teardown(self) -> None:
        self._timer.teardown()


class FadeIn(_FaderTransition):
    _ease = Ease.IN


class FadeOut(_FaderTransition):
    _ease = Ease.OUT
