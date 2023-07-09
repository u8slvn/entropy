from __future__ import annotations

import pygame

from entropy.colors import BLACK


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()
        self.driver = pygame.display.get_driver()


class Resolution:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.flags = 0

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    def __str__(self) -> str:
        return f"{self.width} x {self.height}"


class FullScreenResolution(Resolution):
    def __init__(self, monitor: Monitor):
        super().__init__(width=monitor.info.current_w, height=monitor.info.current_h)
        self.flags = pygame.FULLSCREEN

    def __str__(self):
        return "Fullscreen"


class Window:
    def __init__(self, resolution: Resolution, title: str, fps: float) -> None:
        self.fps = fps
        self.screen = pygame.display.set_mode(resolution.size, resolution.flags)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title=title)

    def process(self, display: pygame.Surface):
        self.screen.fill(BLACK)

        self.screen.blit(
            pygame.transform.scale(display, self.screen.get_size()), (0, 0)
        )
        pygame.display.flip()
        self.clock.tick(self.fps)
