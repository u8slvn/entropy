from __future__ import annotations

from sys import exit
from typing import TYPE_CHECKING

import pygame

import entropy
from entropy import states
from entropy.components.fps import FPS
from entropy.misc.rescaler import ReScaler
from entropy.misc.window import Window


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(self, dimension: tuple[int, int], window: Window) -> None:
        self.dimension = dimension
        self.window = window
        self.rescaler = ReScaler(window=window)
        self.running = False
        self.states: dict[str, State] = {}
        self.state: State | None = None
        self.fps = FPS(entropy.window.clock)

    @property
    def aspect_ratio(self) -> float:
        return self.dimension[0] / self.dimension[1]

    def load(self) -> None:
        entropy.assets.load()
        self.states = states.loads(game=self)
        self.state = self.states["SPLASH"]

    def transition_to(self, state: str) -> None:
        self.state.teardown()
        self.state = self.states[state]

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE and not entropy.window.fullscreen:
                entropy.window.resize(dimension=(event.w, event.h))
                self.state.setup()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    entropy.window.toggle_fullscreen()
                    self.state.setup()
                self.fps.handle_event(event=event)

            self.state.process_event(event=event)

    def update(self):
        self.state.update()
        self.fps.update()

    def draw(self):
        self.state.draw(display=self.window.screen)
        self.fps.draw(display=self.window.screen)
        entropy.window.render()

    def start(self) -> None:
        self.load()
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.draw()

        pygame.quit()
        exit()
