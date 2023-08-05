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
        self._background.set_alpha(self._default_alpha_value())
        self._alpha_rate = 255 / duration

    def _default_alpha_value(self) -> int:
        return 255 if self._ease is Ease.IN else 0

    def _update(self) -> None:
        if self._ease is Ease.IN:
            alpha = max(int(self.countdown * self._alpha_rate), 0)
        else:
            alpha = min(255 - int(self.countdown * self._alpha_rate), 255)
        self._background.set_alpha(alpha)

    def _draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._background, self._background.pos)

    def reset(self) -> None:
        super().reset()
        self._background.set_alpha(self._default_alpha_value())


class FadeIn(_FaderTransition):
    _ease = Ease.IN


class FadeOut(_FaderTransition):
    _ease = Ease.OUT
