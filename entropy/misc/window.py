from __future__ import annotations

import pygame

import entropy
from entropy.utils.display import convert_dimension_to_ratio


class Window:
    def __init__(
        self,
        title: str,
        fps: float,
        dimension: tuple[int, int],
        fullscreen: bool,
    ) -> None:
        self.fps = fps
        self.dimension = dimension
        self.fullscreen = fullscreen
        # The screen is configured for the loader by default
        self.screen = pygame.display.set_mode(dimension, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title=title)

    def refresh_screen(self) -> None:
        if self.fullscreen:
            dimension = convert_dimension_to_ratio(
                ratio=entropy.game.aspect_ratio, dimension=entropy.monitor.size
            )
            self.screen = pygame.display.set_mode(dimension, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.dimension, pygame.RESIZABLE)

    def resize(self, dimension: tuple[int, int]) -> None:
        self.dimension = convert_dimension_to_ratio(
            ratio=entropy.game.aspect_ratio, dimension=dimension
        )
        self.refresh_screen()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.refresh_screen()

    def render(self) -> None:
        pygame.display.flip()
        self.clock.tick(self.fps)
