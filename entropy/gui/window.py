from __future__ import annotations

import logging

import pygame

import entropy

from entropy.gui.monitor import Monitor
from entropy.utils import PosScale
from entropy.utils import Res


logger = logging.getLogger(__name__)


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
        self.monitor = Monitor()
        self.fullscreen = fullscreen
        self.render_res = render_res
        self.screen = self._build_screen(resolution=entropy.config.res)
        self.screen_rect = self.screen.get_rect()
        self.render_scale = PosScale(1.0, 1.0)
        self.update_render_scale()

    def _build_screen(self, resolution: Res) -> pygame.Surface:
        """
        Build screen surface.

        If the given resolution is the same as the monitor resolution the resolution is
        scale down to fit inside the monitor.
        """
        if resolution == self.monitor.res and self.screen_flags != pygame.FULLSCREEN:
            resolution = resolution - Res(80, 75)

        logger.info(
            f"Set display mode: "
            f"resolution = {resolution}, fullscreen = {self.fullscreen}"
        )
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
        self.render_scale = PosScale(
            self.render_res.w / self.screen_rect.w,
            self.render_res.h / self.screen_rect.h,
        )

    def resize_screen(self, resolution: Res | None = None) -> None:
        """Resize the screen to the given resolution size."""
        if self.fullscreen is True:
            resolution = self.adapt_to_ratio(resolution=self.monitor.res)
        elif resolution is None:
            resolution = self.adapt_to_ratio(entropy.config.res)
        else:
            resolution = self.adapt_to_ratio(resolution=resolution)
            entropy.config.res = resolution

        self.screen = self._build_screen(resolution)
        self.screen_rect = self.screen.get_rect()
        self.update_render_scale()

    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen on/off."""
        self.fullscreen = not self.fullscreen
        self.resize_screen()

    def render(self, surface: pygame.Surface) -> None:
        """
        Render the giver surface to the screen.

        If the screen size is not the same size as the render resolution, the surface
        is scaled to the screen size.
        """
        if self.render_res != self.screen_rect.size:
            pygame.transform.scale(surface, self.screen_rect.size, self.screen)
        else:
            self.screen.blit(surface, (0, 0))
        pygame.display.update()
