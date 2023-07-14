from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from entropy.misc.mouse import Mouse
from entropy.utils import Resolution


if TYPE_CHECKING:
    from entropy.misc.window import Window
    from entropy.states import State


class Control:
    def __init__(
        self,
        window: Window,
        fps: float,
        states: dict[str, State],
        state: str,
    ) -> None:
        self.window = window
        self.fps = fps
        self.render_surface = pg.Surface(self.window.render_resolution).convert()
        self.states = states
        self.state = self.states[state]
        self.running = False
        self.clock = pg.time.Clock()
        self.mouse = Mouse(window=window)

    def transition_to(self, state: str) -> None:
        self.state.cleanup()
        self.state = self.states[state]
        self.state.startup(control=self)

    def process_events(self) -> None:
        self.mouse.update_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE and not self.window.fullscreen:
                self.window.resize_screen(resolution=Resolution(event.w, event.h))
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.window.toggle_fullscreen()
            self.state.handle_event(event=event)

    def update(self) -> None:
        self.state.update()

    def render(self) -> None:
        self.state.draw(surface=self.render_surface)
        self.window.render(surface=self.render_surface)

    def start(self) -> None:
        self.running = True
        self.state.startup(control=self)

        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        pg.quit()
        exit()
