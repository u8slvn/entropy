from __future__ import annotations

import pygame

from entropy.commands.base import Command


class QuitGame(Command):
    def __call__(self) -> None:
        event = pygame.Event(type=pygame.QUIT)
        pygame.event.post(event=event)
