from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import states
from entropy.misc.assets import Assets
from entropy.misc.resolution import Resolution, r720P, r900P
from entropy.misc.scale import Scaler


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(
        self,
        title: str,
        fps: float,
        screen_resolution: Resolution,
        max_resolution: Resolution,
        fullscreen: bool,
    ) -> None:
        self.fps = fps
        self.screen_resolution = screen_resolution
        self.max_resolution = max_resolution
        self.fullscreen = fullscreen

        pygame.display.set_caption(title=title)

        self.running = False

        self.states: dict[str, State] = {}
        self.state: State | None = None

        self.screen = pygame.display.set_mode(screen_resolution.size)
        self.clock = pygame.time.Clock()

        self.scaler = Scaler(game=self)
        self.assets = Assets(game=self)

    def load(self) -> None:
        self.assets.load()
        self.states = states.loads(game=self)
        self.state = self.states["SPLASH"]

    def transition_to(self, state: str) -> None:
        self.state.teardown()
        self.state = self.states[state]

    def resize_screen(
        self, resolution: Resolution | None = None, fullscreen=False
    ) -> None:
        self.fullscreen = fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                self.max_resolution.size, pygame.FULLSCREEN
            )
        else:
            self.screen_resolution = resolution or self.screen_resolution
            self.screen = pygame.display.set_mode(self.screen_resolution.size)

        self.assets.scale()
        self.state.setup()

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    print("press f")
                    self.resize_screen(fullscreen=True)
                elif event.key == pygame.K_q:
                    print("press q")
                    self.resize_screen(resolution=r720P)
                elif event.key == pygame.K_e:
                    print("press e")
                    self.resize_screen(resolution=r900P)

            self.state.process_event(event=event)

    def update(self):
        self.state.update()

    def render(self):
        self.state.draw(display=self.screen)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def start(self) -> None:
        self.load()
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.render()

        pygame.quit()
        exit()
