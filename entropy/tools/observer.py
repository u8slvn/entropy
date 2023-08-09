from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Observer(ABC):
    @abstractmethod
    def on_notify(self) -> None:
        ...


class Subject(ABC):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)
        observer.on_notify()

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.on_notify()
