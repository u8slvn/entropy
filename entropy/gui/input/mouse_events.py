from __future__ import annotations

import pygame


class MouseEvents:
    def __init__(self) -> None:
        self.BUTTON1 = False
        self.BUTTON2 = False
        self.BUTTON3 = False

    def parse_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.BUTTON1 = True
            elif event.button == 2:
                self.BUTTON2 = True
            elif event.button == 2:
                self.BUTTON3 = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.BUTTON1 = False
            elif event.button == 2:
                self.BUTTON2 = False
            elif event.button == 2:
                self.BUTTON3 = False

    def reset(self) -> None:
        for event in self.__dict__.keys():
            setattr(self, event, False)
