from __future__ import annotations

import pygame

from entropy.gui.input import InputsController


class KeyboardInputs(InputsController):
    def __init__(self):
        self.KEYDOWN = False
        self.KEYUP = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.ENTER = False
        self.SPACE = False
        self.F5 = False
        self.F6 = False

    def parse_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.KEYDOWN = True
            if event.key == pygame.K_UP:
                self.UP = True
            elif event.key == pygame.K_DOWN:
                self.DOWN = True
            elif event.key == pygame.K_LEFT:
                self.LEFT = True
            elif event.key == pygame.K_RIGHT:
                self.RIGHT = True
            elif event.key == pygame.K_RETURN:
                self.ENTER = True
            elif event.key == pygame.K_SPACE:
                self.SPACE = True
            elif event.key == pygame.K_F5:
                self.F5 = True
            elif event.key == pygame.K_F6:
                self.F6 = True

        if event.type == pygame.KEYUP:
            self.KEYUP = True
            if event.key == pygame.K_UP:
                self.UP = False
            elif event.key == pygame.K_DOWN:
                self.DOWN = False
            elif event.key == pygame.K_LEFT:
                self.LEFT = False
            elif event.key == pygame.K_RIGHT:
                self.RIGHT = False
            elif event.key == pygame.K_RETURN:
                self.ENTER = False
            elif event.key == pygame.K_SPACE:
                self.SPACE = False
            elif event.key == pygame.K_F5:
                self.F5 = False
            elif event.key == pygame.K_F6:
                self.F6 = False

    def flush(self) -> None:
        for event in self.__dict__.keys():
            setattr(self, event, False)
