from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy.colors import BLACK


if TYPE_CHECKING:
    from entropy.misc.resolution import Resolution


class Window:
    def __init__(
        self, resolution: Resolution, fps: float, title: str, aspect_ratio: float
    ) -> None:
        self.screen = pygame.display.set_mode(resolution.size, resolution.flags)
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.aspect_ratio = aspect_ratio

        pygame.display.set_caption(title=title)

    def resize(self, resolution: Resolution):
        self.screen = pygame.display.set_mode(resolution.size, resolution.flags)

    @property
    def aspect_ratio_size(self) -> tuple[int, int]:
        screen_w, screen_h = self.screen.get_size()

        if screen_w / screen_h == self.aspect_ratio:
            return screen_w, screen_h
        elif screen_h > screen_w / self.aspect_ratio:
            return screen_w, int(screen_w / self.aspect_ratio)
        else:
            return int(screen_h * self.aspect_ratio), screen_h

    def draw(self, display: pygame.Surface):
        self.screen.fill(BLACK)
        self.screen.blit(
            pygame.transform.scale(display, self.aspect_ratio_size), (0, 0)
        )
        pygame.display.flip()
        self.clock.tick(self.fps)
