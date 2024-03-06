from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Command(ABC):
    """
    Encapsulate an action in order to pass it to an object that can execute it later.
    """

    @abstractmethod
    def __call__(self) -> None: ...


class Commands(list[Command], Command):
    """Chain a list of command."""

    def __call__(self) -> None:
        for command in self:
            command()
