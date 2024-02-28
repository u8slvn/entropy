from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Command(ABC):
    @abstractmethod
    def __call__(self) -> None: ...


class ConfigurableCommand(Command, ABC):
    def __init__(self) -> None:
        self._args = ()

    def configure(self, *args) -> None:
        self._args = args

    @abstractmethod
    def __call__(self) -> None: ...


class Commands(list, Command):
    def __call__(self) -> None:
        while self:
            command = self.pop()
            command()
