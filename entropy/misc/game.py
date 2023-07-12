from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy
from entropy.misc.monitor import Monitor
from entropy.states import states
from entropy.utils.display import dimension_to_ratio


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(
        self,
        title: str,
        fps: float,
        render_resolution: tuple[int, int],
        fullscreen: bool,
    ) -> None:
        pg.display.set_caption(title=title)
        self.screen = pg.display.set_mode(render_resolution, pg.RESIZABLE)
        self.screen_rect = self.screen.get_rect()
        self.render_resolution = render_resolution
        self.render_surface = pg.Surface(self.render_resolution).convert()
        self.aspect_ratio = render_resolution[0] / render_resolution[1]
        self.monitor = Monitor()
        self.fps = fps
        self.fullscreen = fullscreen
        self.running = False
        self.states: dict[str, State] = {}
        self.state: State | None = None
        self.clock = pg.time.Clock()

    def setup(self) -> None:
        entropy.assets.load()
        self.transition_to("SPLASH")

    def transition_to(self, state_name: str) -> None:
        if self.state is not None:
            self.state.teardown()
        self.state = states[state_name](game=self)

    def resize_screen(self, dimension: tuple[int, int]) -> None:
        dimension = dimension_to_ratio(dimension=dimension, ratio=self.aspect_ratio)
        flags = pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE
        self.screen = pg.display.set_mode(dimension, flags)
        self.screen_rect = self.screen.get_rect()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.resize_screen(dimension=self.render_resolution)
        else:
            dimension = int(self.monitor.w // 1.5), int(self.monitor.h // 1.5)
            self.resize_screen(dimension=dimension)

    def process_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE and not self.fullscreen:
                self.resize_screen(dimension=(event.w, event.h))
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.toggle_fullscreen()
            self.state.process_event(event=event)

    def update(self):
        self.state.update()

    def render(self):
        self.state.draw(surface=self.render_surface)
        if self.render_resolution != self.screen_rect.size:
            pg.transform.smoothscale(
                self.render_surface, self.screen_rect.size, self.screen
            )
        else:
            self.screen.blit(self.render_surface, (0, 0))
        pg.display.update()
        self.clock.tick(self.fps)

    def start(self) -> None:
        self.setup()
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.render()

        pg.quit()
        exit()
