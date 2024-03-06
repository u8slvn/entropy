from __future__ import annotations

import time

from types import MappingProxyType
from typing import Any
from typing import Iterator


class EventMapping:
    def __init__(self, mapping: dict[int, int]):
        self._mapping = MappingProxyType(mapping)

    def get(self, event: int) -> int | None:
        return self._mapping.get(event)


class Event:
    __slots__ = ("key", "value", "pressed", "released", "triggered", "time")

    def __init__(self, key: int, value: Any = 1):
        self.key = key
        self.value = value
        self.pressed = False
        self.released = False
        self.triggered = False
        self.time = None

    @property
    def held(self) -> bool:
        return bool(self.value)

    @property
    def hold_time(self) -> float:
        return 0 if self.time is None else time.time() - self.time

    def __repr__(self) -> str:
        return f"PlayerInput<{self.key}, {self.pressed}, {self.released}, {self.triggered}, {self.value}, {self.hold_time}>"


class EventStore(dict[int, Event]):
    def __missing__(self, key) -> Event:
        self[key] = Event(key)
        return self[key]

    def __iter__(self) -> Iterator[Event]:
        return iter(self.values())

    def flush(self) -> None:
        self.clear()
