from __future__ import annotations

import pygame

from entropy.gui.input import InputsController


class MouseInputs(InputsController):
    def __init__(self) -> None:
        self.BUTTON1 = False
        self.BUTTON2 = False
        self.BUTTON3 = False
        self.POS: tuple[int, int] | None = None

    def parse_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.POS = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.BUTTON1 = True
            elif event.button == 2:
                self.BUTTON2 = True
            elif event.button == 2:
                self.BUTTON3 = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.BUTTON1 = False
            elif event.button == 2:
                self.BUTTON2 = False
            elif event.button == 2:
                self.BUTTON3 = False

    def flush(self) -> None:
        self.BUTTON1 = False
        self.BUTTON2 = False
        self.BUTTON3 = False
        self.POS = None
