from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Command(ABC):
    @abstractmethod
    def __call__(self) -> None: ...


class Commands(list, Command):
    def __call__(self) -> None:
        for command in self:
            command()
