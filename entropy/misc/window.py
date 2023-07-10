from __future__ import annotations

import pygame

import entropy
from entropy.misc.loader import Loader
from entropy.utils.display import convert_size_to_ratio


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
        self.screen = pygame.display.set_mode(Loader.dimension, pygame.NOFRAME)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(title=title)

    def refresh_screen(self) -> None:
        if self.fullscreen:
            size = convert_size_to_ratio(
                ratio=entropy.game.aspect_ratio, size=entropy.monitor.size
            )
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.dimension, pygame.RESIZABLE)

    def resize(self, dimension: tuple[int, int]):
        self.dimension = dimension
        self.refresh_screen()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.refresh_screen()

    def draw(self, display: pygame.Surface, keep_ratio: bool = True):
        if keep_ratio:
            screen_size = self.screen.get_size()
            display_size = convert_size_to_ratio(
                ratio=entropy.game.aspect_ratio, size=screen_size
            )

            self.screen.blit(
                pygame.transform.scale(display, display_size),
                (
                    (screen_size[0] - display_size[0])
                    // 2,  # center w display in screen
                    (screen_size[1] - display_size[1])
                    // 2,  # center h display in screen
                ),
            )
        else:
            self.screen.blit(display, (0, 0))

        pygame.display.flip()
        self.clock.tick(self.fps)
