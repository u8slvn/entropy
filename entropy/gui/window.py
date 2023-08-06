from __future__ import annotations

import pygame

from entropy.gui.monitor import Monitor
from entropy.utils import Res
from entropy.utils import Scale


class Window:
    """
    Window manager.

    Manage the whole game window related actions.
    """

    def __init__(
        self,
        title: str,
        fullscreen: bool,
        render_res: Res,
    ) -> None:
        pygame.display.set_caption(title)
        self.fullscreen = fullscreen
        self.render_res = render_res
        self.screen = self._build_screen(self.render_res)
        self.screen_rect = self.screen.get_rect()
        self.render_scale = Scale(1.0, 1.0)
        self.monitor = Monitor()
        self.update_render_scale()

    def _build_screen(self, resolution: Res) -> pygame.Surface:
        """
        Build screen surface.

        If the given resolution is the same as the render resolution the resolution is
        scale down to fit inside the monitor.
        """
        if resolution == self.render_res:
            resolution = resolution - Res(80, 75)

        return pygame.display.set_mode(resolution, self.screen_flags)

    @property
    def screen_flags(self) -> int:
        """Return rhe screen mode flags."""
        return pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

    def adapt_to_ratio(self, resolution: Res) -> Res:
        """Adapt the given resolution to the render resolution ratio."""
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
        """
        Update the rander scale.

        Used to scale the mouse position to match the display resolution.
        """
        self.render_scale = Scale(
            self.render_res.w / self.screen_rect.w,
            self.render_res.h / self.screen_rect.h,
        )

    def resize_screen(self, resolution: Res) -> None:
        """Resize the screen to the given resolution size."""
        resolution = self.adapt_to_ratio(resolution=resolution)
        self.screen = self._build_screen(resolution)
        self.screen_rect = self.screen.get_rect()
        self.update_render_scale()

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen on/off."""
        self.fullscreen = not self.fullscreen
        self.resize_screen(resolution=self.render_res)

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the giver surface to the screen.

        If the screen size is not the same size as the render resolution, the surface
        is scaled to the screen size.
        """
        if self.render_res != self.screen_rect.size:
            pygame.transform.smoothscale(surface, self.screen_rect.size, self.screen)
        else:
            self.screen.blit(surface, (0, 0))
        pygame.display.update()
