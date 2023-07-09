from __future__ import annotations

from sys import exit
from typing import TYPE_CHECKING

import pygame

import entropy
from entropy import states
from entropy.components.fps import FPS


if TYPE_CHECKING:
    from entropy.states import State


class Game:
    def __init__(self) -> None:
        self.display = pygame.Surface((1920, 1080))
        self.running = False
        self.states: dict[str, State] = {}
        self.state: State | None = None
        self.fps = FPS(entropy.window.clock)

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
            elif event.type == pygame.VIDEORESIZE:
                entropy.window.resize(dimension=(event.w, event.h))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    entropy.window.toggle_fullscreen()
                self.fps.toggle(key=event.key)

            self.state.process_event(event=event)

    def update(self):
        self.state.update()
        self.fps.update()

    def render(self):
        self.state.render(self.display)
        self.fps.render(self.display)
        entropy.window.draw(self.display)

    def start(self) -> None:
        self.running = True
        self.load()

        while self.running:
            self.process_events()
            self.update()
            self.render()

        pygame.quit()
        exit()
