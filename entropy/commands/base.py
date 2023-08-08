from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Command(ABC):
    @abstractmethod
    def __call__(self):
        ...


class Commands(list, Command):
    def __setitem__(self, index: int, command: Command) -> None:
        super().__setitem__(index, command)

    def insert(self, index: int, command: Command) -> None:
        super().insert(index, command)

    def append(self, command: Command) -> None:
        super().append(command)

    def __call__(self):
        while self:
            command = self.pop()
            command()
