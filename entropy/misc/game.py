from __future__ import annotations

from sys import exit
from typing import TYPE_CHECKING

import pygame

from entropy.components.fps import FPS
from entropy.misc.window import Monitor, Resolution, Window


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(self, title: str, monitor: Monitor) -> None:
        self.window = Window(title=title, resolution=Resolution(1280, 720), fps=60)
        self.display = pygame.Surface((1920, 1080))
        self.monitor = monitor
        self.running = False
        self.states: dict[str, State] = {}
        self.state: State | None = None
        self.resolutions = dict[str, Resolution]
        self.fps = FPS(self.window.clock)

    def setup_states(
        self, states: dict[str, State], default_state: str = "SPLASH"
    ) -> None:
        self.states = states
        self.state = self.states[default_state]

    def setup_resolution(
        self, resolutions: dict[str, Resolution], default_resolution: str
    ) -> None:
        self.resolutions = resolutions

    def transition_to(self, state: str) -> None:
        self.state.teardown()
        self.state = self.states[state]

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                self.fps.toggle(key=event.key)

            self.state.process_event(event=event)

    def update(self):
        self.state.update()
        self.fps.update()

    def render(self):
        self.state.render(self.display)
        self.fps.render(self.display)
        self.window.process(self.display)

    def start(self) -> None:
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.render()

        pygame.quit()
        exit()
