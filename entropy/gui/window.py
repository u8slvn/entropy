from __future__ import annotations

import pygame

from entropy.gui.monitor import Monitor
from entropy.utils import Res
from entropy.utils import Scale


class Window:
    def __init__(
        self,
        title: str,
        fullscreen: bool,
        render_res: Res,
    ) -> None:
        pygame.display.set_caption(title)
        self.fullscreen = fullscreen
        self.render_res = render_res
        self.screen = pygame.display.set_mode(self.render_res, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.render_scale = Scale(1.0, 1.0)
        self.monitor = Monitor()

    @property
    def screen_flags(self) -> int:
        return pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

    def adapt_to_ratio(self, resolution: Res) -> Res:
        if resolution.aspect_ratio == self.render_res.aspect_ratio:
            return resolution
        elif resolution.h > resolution.w / self.render_res.aspect_ratio:
            return Res(
                w=resolution.w,
                h=int(resolution.w / self.render_res.aspect_ratio),
            )
        else:
            return Res(
                w=int(resolution.h * self.render_res.aspect_ratio),
                h=resolution.h,
            )

    def update_render_scale(self) -> None:
        self.render_scale = Scale(
            self.render_res.w / self.screen_rect.w,
            self.render_res.h / self.screen_rect.h,
        )

    def resize_screen(self, resolution: Res) -> None:
        dimension = self.adapt_to_ratio(resolution=resolution)
        self.screen = pygame.display.set_mode(dimension, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.update_render_scale()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.resize_screen(resolution=self.render_res)

    def render(self, surface: pygame.Surface) -> None:
        if self.render_res != self.screen_rect.size:
            pygame.transform.smoothscale(surface, self.screen_rect.size, self.screen)
        else:
            self.screen.blit(surface, (0, 0))
        pygame.display.update()
