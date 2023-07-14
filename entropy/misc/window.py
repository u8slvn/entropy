from __future__ import annotations

import pygame as pg

from entropy.misc.monitor import Monitor
from entropy.utils import Resolution, Scale


class Window:
    def __init__(
        self,
        title: str,
        fullscreen: bool,
        render_resolution: Resolution,
    ) -> None:
        pg.display.set_caption(title=title)
        self.fullscreen = fullscreen
        self.screen = pg.display.set_mode(render_resolution, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.render_resolution = render_resolution
        self.render_scale = Scale(1.0, 1.0)
        self.monitor = Monitor()

    @property
    def screen_flags(self) -> int:
        return pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE

    def adapt_to_ratio(self, resolution: Resolution) -> Resolution:
        if resolution.aspect_ratio == self.render_resolution.aspect_ratio:
            return resolution
        elif resolution.h > resolution.w / self.render_resolution.aspect_ratio:
            return Resolution(
                w=resolution.w,
                h=int(resolution.w / self.render_resolution.aspect_ratio),
            )
        else:
            return Resolution(
                w=int(resolution.h * self.render_resolution.aspect_ratio),
                h=resolution.h,
            )

    def update_render_scale(self) -> None:
        self.render_scale = Scale(
            self.render_resolution.w / self.screen_rect.w,
            self.render_resolution.h / self.screen_rect.h,
        )

    def resize_screen(self, resolution: Resolution) -> None:
        dimension = self.adapt_to_ratio(resolution=resolution)
        self.screen = pg.display.set_mode(dimension, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.update_render_scale()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.resize_screen(resolution=self.render_resolution)

    def render(self, surface: pg.Surface) -> None:
        if self.render_resolution != self.screen_rect.size:
            pg.transform.smoothscale(surface, self.screen_rect.size, self.screen)
        else:
            self.screen.blit(surface, (0, 0))
        pg.display.update()
