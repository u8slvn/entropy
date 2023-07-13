from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import entropy
from entropy import states
from entropy.misc.monitor import Monitor
from entropy.utils import dimension_to_ratio


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(
        self,
        title: str,
        fps: float,
        fullscreen: bool,
        render_resolution: tuple[int, int],
    ) -> None:
        pg.display.set_caption(title=title)
        self.fps = fps
        self.fullscreen = fullscreen
        self.screen = pg.display.set_mode(render_resolution, self.screen_flags)
        self.screen_rect = self.screen.get_rect()
        self.render_resolution = render_resolution
        self.render_surface = pg.Surface(self.render_resolution).convert()
        self.aspect_ratio = render_resolution[0] / render_resolution[1]
        self.monitor = Monitor()
        self.running = False
        self.states: dict[str:State] | None = None
        self.state: State | None = None
        self.clock = pg.time.Clock()

    @property
    def screen_flags(self) -> int:
        return pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE

    def startup(self) -> None:
        entropy.assets.load()
        self.states = states.load()
        self.transition_to("SPLASH")

    def transition_to(self, state: str) -> None:
        if self.state is not None:
            self.state.cleanup()
        self.state = self.states.get(state)
        self.state.startup(game=self)

    def resize_screen(self, dimension: tuple[int, int]) -> None:
        dimension = dimension_to_ratio(dimension=dimension, ratio=self.aspect_ratio)
        self.screen = pg.display.set_mode(dimension, self.screen_flags)
        self.screen_rect = self.screen.get_rect()

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.resize_screen(dimension=self.render_resolution)

    def process_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.VIDEORESIZE and not self.fullscreen:
                self.resize_screen(dimension=(event.w, event.h))
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    self.toggle_fullscreen()
            self.state.handle_event(event=event, mouse_pos=(0, 0))

    def update(self) -> None:
        self.state.update()

    def render(self) -> None:
        self.state.draw(surface=self.render_surface)
        if self.render_resolution != self.screen_rect.size:
            pg.transform.smoothscale(
                self.render_surface, self.screen_rect.size, self.screen
            )
        else:
            self.screen.blit(self.render_surface, (0, 0))
        pg.display.update()

    def start(self) -> None:
        self.startup()
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        pg.quit()
        exit()
