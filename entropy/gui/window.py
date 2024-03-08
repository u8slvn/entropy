from __future__ import annotations

import pygame

import entropy

from entropy.gui.monitor import Monitor
from entropy.logging import get_logger
from entropy.utils.measure import Pos
from entropy.utils.measure import PosScale
from entropy.utils.measure import Res
from entropy.utils.pygame import reset_display


logger = get_logger()


class Window:
    """Window manager."""

    _fullscreen_flags = pygame.FULLSCREEN | pygame.SCALED
    _framed_flags = pygame.RESIZABLE

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
        resolution = self.monitor.res if self.fullscreen else entropy.config.res
        self.render_res = self.adapt_to_ratio(resolution)
        self.render_scale = PosScale(1.0, 1.0)
        self.render_margin = Pos(0, 0)
        self.screen = self._build_screen(resolution=self.render_res)
        self.screen_rect = self.screen.get_rect()
        self.update_scale_params()

    @reset_display
    def _build_screen(self, resolution: Res) -> pygame.Surface:
        """
        Build screen surface.

        If the given resolution is the same as the monitor resolution the resolution is
        scale down to fit inside the monitor.
        """
        if (
            resolution == self.monitor.res
            and self.screen_flags != self._fullscreen_flags
        ):
            resolution = resolution - Res(80, 75)

        fullscreen = '"fullscreen", ' if self.fullscreen else ""
        logger.info(f'Display mode set to {fullscreen}"{resolution}"')
        return pygame.display.set_mode(resolution, flags=self.screen_flags)

    @property
    def screen_res(self) -> Res:
        return Res(*self.screen_rect.size)

    @property
    def screen_flags(self) -> int:
        """Return rhe screen mode flags."""
        return self._fullscreen_flags if self.fullscreen else self._framed_flags

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
        if resolution is not None and self.screen_res == resolution:
            logger.debug(
                "Screen not resized because it already fits the given resolution."
            )
            return

        if self.fullscreen:
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
        logger.debug("Fullscreen toggled.")
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
