from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar


T = TypeVar("T")


class Observer(Generic[T], ABC):
    def __init__(self) -> None:
        self._registered_subjects: list[T] = []

    def register(self, subject: T) -> None:
        self._registered_subjects.append(subject)

    @abstractmethod
    def notify(self) -> None:
        ...
