from __future__ import annotations

import pygame as pg

from entropy.utils import Pos


class FPSViewer:
    font_color = "white"
    background_color = "black"

    def __init__(self, clock: pg.time.Clock) -> None:
        self.clock = clock
        self.font = pg.font.SysFont("Arial", 16)
        self.visible = False
        self.fps = 0.0
        self.format = "{fps} FPS"
        self.text = self.font.render("0", True, self.font_color, self.background_color)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYUP and event.key == pg.K_F5:
            self.visible = not self.visible

    def _render_text(self) -> pg.Surface:
        text = self.format.format(fps=round(self.fps))
        return self.font.render(text, True, self.font_color, self.background_color)

    def update(self) -> None:
        if self.visible:
            self.fps = self.clock.get_fps()
            self.text = self._render_text()
            self.text.set_alpha(200)

    def draw(self, surface: pg.Surface) -> None:
        if self.visible:
            pos = Pos(
                surface.get_width() - self.text.get_width(),
                surface.get_height() - self.text.get_height(),
            )
            surface.blit(self.text, pos)
