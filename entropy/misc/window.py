from __future__ import annotations

import pygame

import entropy


class Window:
    def __init__(
        self,
        title: str,
        fps: float,
        aspect_ratio: float,
        dimension: tuple[int, int],
        fullscreen: bool,
    ) -> None:
        self.fps = fps
        self.aspect_ratio = aspect_ratio
        self.dimension = dimension
        self.fullscreen = fullscreen
        self.screen = self._build_screen()
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title=title)

    def _build_screen(self) -> pygame.Surface:
        if self.fullscreen:
            return pygame.display.set_mode(
                self.convert_to_screen_ratio(entropy.monitor.size),
                pygame.FULLSCREEN,
            )

        return pygame.display.set_mode(self.dimension, pygame.RESIZABLE)

    def resize(self, dimension: tuple[int, int]):
        self.dimension = dimension
        self.screen = self._build_screen()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.screen = self._build_screen()

    def convert_to_screen_ratio(self, size: tuple[int, int]) -> tuple[int, int]:
        width, height = size

        if width / height == self.aspect_ratio:
            return width, height
        elif height > width / self.aspect_ratio:
            return width, int(width / self.aspect_ratio)
        else:
            return int(height * self.aspect_ratio), height

    def draw(self, display: pygame.Surface):
        screen_size = self.screen.get_size()
        display_size = self.convert_to_screen_ratio(size=screen_size)

        self.screen.blit(
            pygame.transform.scale(display, display_size),
            (
                (screen_size[0] - display_size[0]) // 2,  # center w display in screen
                (screen_size[1] - display_size[1]) // 2,  # center h display in screen
            ),
        )

        pygame.display.flip()
        self.clock.tick(self.fps)
