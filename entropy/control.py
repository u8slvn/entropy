from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg


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

    def transition_to(self, state: str) -> None:
        self.state.cleanup()
        self.state = self.states[state]
        self.state.startup(control=self)

    def process_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE and not self.window.fullscreen:
                self.window.resize_screen(dimension=(event.w, event.h))
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.window.toggle_fullscreen()
            self.state.handle_event(event=event, mouse_pos=(0, 0))

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
