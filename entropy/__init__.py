import pygame
from sys import exit

from entropy.components.fps import FPS

pygame.init()


class Game:
    def __init__(self, title: str) -> None:
        self.title = title
        self.show_fps = False
        self.running = False
        self.screen_size = (800, 600)
        self.fps = FPS(60.0)

        pygame.display.set_caption(title=self.title)
        self.screen = pygame.display.set_mode(self.screen_size)

    def display_fps(self):
        if self.show_fps is True:
            self.fps.render(self.screen)

    def toggle_show_fps(self, key):
        if key == pygame.K_F5:
            self.show_fps = not self.show_fps

    def get_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                self.toggle_show_fps(event.key)
            elif event.type == pygame.KEYDOWN:
                ...

    def update(self):
        self.screen.fill((0, 0, 0))

    def render(self):
        self.display_fps()
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
