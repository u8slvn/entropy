from sys import exit

import pygame

from entropy.components.fps import FPS
from entropy.display import Screen, Resolution, Monitor, FullScreenResolution

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

        pygame.display.set_caption(title=self.title)

    def get_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                self.fps.toggle(key=event.key)
            elif event.type == pygame.KEYDOWN:
                ...

    def update(self):
        self.fps.update()

    def render(self):
        self.fps.render(self.screen.display)
        pygame.display.update()
        self.fps.tick()

    def start(self) -> None:
        self.running = True

        while self.running:
            self.get_events()
            self.update()
            self.render()

        pygame.quit()
        exit()
