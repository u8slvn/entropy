from __future__ import annotations

import pygame

import entropy

from entropy.gui.monitor import Monitor
from entropy.logger import get_logger
from entropy.utils import Pos
from entropy.utils import PosScale
from entropy.utils import Res


logger = get_logger()


class Window:
    """
    Window manager.

    Manage the whole game window related actions.
    """

    def __init__(
        self,
        title: str,
        fullscreen: bool,
        default_res: Res,
    ) -> None:
        pygame.display.set_caption(title)
        self.monitor = Monitor()
        self.fullscreen = fullscreen
        self.default_res = default_res
        self.render_res = self.adapt_to_ratio(entropy.config.res)
        self.render_scale = PosScale(1.0, 1.0)
        self.render_margin = Pos(0, 0)
        self.screen = self._build_screen(resolution=self.render_res)
        self.screen_rect = self.screen.get_rect()

        if self.fullscreen is True:
            self.resize_screen()
        self.update_scale_params()

    def _build_screen(self, resolution: Res) -> pygame.Surface:
        """
        Build screen surface.

        If the given resolution is the same as the monitor resolution the resolution is
        scale down to fit inside the monitor.
        """
        if resolution == self.monitor.res and self.screen_flags != pygame.FULLSCREEN:
            resolution = resolution - Res(80, 75)

        logger.info(
            f'Display mode set to "{resolution}"'
            f"{['', ' - fullscreen'][self.fullscreen]}."
        )
        return pygame.display.set_mode(resolution, self.screen_flags)

    @property
    def screen_flags(self) -> int:
        """Return rhe screen mode flags."""
        return pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE

    def adapt_to_ratio(self, resolution: Res) -> Res:
        """Adapt the given resolution to the render resolution ratio."""
        if resolution.aspect_ratio == self.default_res.aspect_ratio:
            return resolution
        elif resolution.h > resolution.w / self.default_res.aspect_ratio:
            return Res(
                w=resolution.w,
                h=int(resolution.w / self.default_res.aspect_ratio),
            )
        else:
            return Res(
                w=int(resolution.h * self.default_res.aspect_ratio),
                h=resolution.h,
            )

    def update_scale_params(self) -> None:
        """
        Update the scale params.

        Used to scale the mouse position to match the display resolution.
        """
        margin_x = (self.screen_rect.w - self.render_res.w) // 2
        margin_y = (self.screen_rect.h - self.render_res.h) // 2
        self.render_margin = Pos(margin_x, margin_y)
        self.render_scale = PosScale(
            self.default_res.w / self.render_res.w,
            self.default_res.h / self.render_res.h,
        )

    def resize_screen(self, resolution: Res | None = None) -> None:
        """Resize the screen to the given resolution size."""
        if self.fullscreen is True:
            resolution = self.monitor.res
        elif resolution is None:
            resolution = entropy.config.res
        else:
            entropy.config.res = resolution

        self.screen = self._build_screen(resolution)
        self.screen_rect = self.screen.get_rect()
        self.render_res = self.adapt_to_ratio(resolution)
        self.update_scale_params()

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
        if self.default_res != self.screen_rect.size:
            surface = pygame.transform.scale(surface, self.render_res)

        surf_rect = surface.get_rect()
        surf_rect.center = self.screen_rect.center
        self.screen.blit(surface, surf_rect)
        pygame.display.update()
