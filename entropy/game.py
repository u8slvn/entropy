from __future__ import annotations

from sys import exit
from typing import TYPE_CHECKING, Type

import pygame

from entropy.components.fps import FPS
from entropy.display import FullScreenResolution, Monitor, Resolution, Screen
from entropy.states.splash import Splash


if TYPE_CHECKING:
    from entropy.states import State

pygame.init()

MONITOR = Monitor()

SD = Resolution(width=720, height=480)
SHD = Resolution(width=1280, height=720)
FHD = Resolution(width=1920, height=1080)
FULLSCREEN = FullScreenResolution(monitor=MONITOR)

RESOLUTIONS = [SD, SHD, FHD, FULLSCREEN]


class Game:
    def __init__(self, title: str) -> None:
        self.title = title
        self.running = False
        self.fps = FPS(60.0)
        self.screen = Screen(resolution=SHD)
        self.state = Splash(game=self)

        pygame.display.set_caption(title=self.title)

    def transition_to(self, state: Type[State]):
        self.state.teardown()
        self.state = state(self)

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
        self.state.draw(self.screen.display)
        self.fps.render(self.screen.display)
        pygame.display.update()
        self.fps.tick()

    def start(self) -> None:
        self.running = True

        while self.running:
            self.process_events()
            self.update()
            self.render()

        pygame.quit()
        exit()
