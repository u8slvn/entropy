from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Observer(ABC):
    @abstractmethod
    def on_notify(self) -> None: ...


class Subject(ABC):
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.on_notify()
