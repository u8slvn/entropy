from __future__ import annotations

import pygame

from entropy.gui.input.base import InputsController
from entropy.gui.input.keyboard_inputs import KeyboardInputs
from entropy.gui.input.mouse_inputs import MouseInputs


class Inputs(InputsController):
    def __init__(
        self,
    ):
        self.keyboard = KeyboardInputs()
        self.mouse = MouseInputs()

    def parse_event(self, event: pygame.event.Event) -> None:
        self.keyboard.parse_event(event=event)
        self.mouse.parse_event(event=event)

    def flush(self):
        self.keyboard.flush()
        self.mouse.flush()
