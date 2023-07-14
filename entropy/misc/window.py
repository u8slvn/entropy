from __future__ import annotations

import pygame as pg

from entropy.misc.monitor import Monitor


class Window:
    def __init__(
        self,
        title: str,
        fullscreen: bool,
        render_resolution: tuple[int, int],
    ) -> None:
        pg.display.set_caption(title=title)
        self.fullscreen = fullscreen
        self.screen = pg.display.set_mode(render_resolution, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.render_resolution = render_resolution
        self.render_scale = (1.0, 1.0)
        self.aspect_ratio = render_resolution[0] / render_resolution[1]
        self.monitor = Monitor()

    @property
    def screen_flags(self) -> int:
        return pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE

    def adapt_to_ratio(self, dimension: tuple[int, int]) -> tuple[int, int]:
        width, height = dimension
        if width / height == self.aspect_ratio:
            return width, height
        elif height > width / self.aspect_ratio:
            return width, int(width / self.aspect_ratio)
        else:
            return int(height * self.aspect_ratio), height

    def update_render_scale(self) -> None:
        self.render_scale = (
            self.render_resolution[0] / self.screen_rect.w,
            self.render_resolution[1] / self.screen_rect.h,
        )

    def resize_screen(self, dimension: tuple[int, int]) -> None:
        dimension = self.adapt_to_ratio(dimension=dimension)
        self.screen = pg.display.set_mode(dimension, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.update_render_scale()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.resize_screen(dimension=self.render_resolution)

    def render(self, surface: pg.Surface) -> None:
        if self.render_resolution != self.screen_rect.size:
            pg.transform.smoothscale(surface, self.screen_rect.size, self.screen)
        else:
            self.screen.blit(surface, (0, 0))
        pg.display.update()
