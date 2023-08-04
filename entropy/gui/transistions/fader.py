from __future__ import annotations

import pygame

from entropy.utils import Timer


class FadeIn:
    def __init__(self, dimension: tuple[int, int], duration: int) -> None:
        background = pygame.Surface(dimension, pygame.SRCALPHA, 32)
        background.fill((0, 0, 0, 255))
        self._background = background.convert_alpha()
        self._timer = Timer(countdown=duration)
        self._timer.start()
        self._alpha_rate = 255 / duration

    def update(self) -> None:
        if self._timer.is_finished():
            return

        self._timer.update()
        alpha = max(int(self._timer.countdown * self._alpha_rate), 0)
        print(alpha)
        self._background.set_alpha(alpha)

    def draw(self, surface: pygame.Surface) -> None:
        if self._timer.is_finished():
            return

        surface.blit(self._background, (0, 0))
