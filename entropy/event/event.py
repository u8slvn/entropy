from __future__ import annotations

import time

from types import MappingProxyType
from typing import Any
from typing import Iterator


class EventMapping:
    """Represent the mapping between game event and pygame event."""

    def __init__(self, mapping: dict[int, int]):
        self._mapping = MappingProxyType(mapping)

    def get(self, event: int) -> int | None:
        return self._mapping.get(event)


class Event:
    """
    Represent a game event.
      - Key is the name by which the event is referred in the game.
      - Value is the value that can be associate to the event, like the mouse position.
      - Pressed handle the press status for a button.
      - Released handle the release status for a button.
      - Triggered handle the trigger status for a standalone event.
      - Time is the time in second when a button has been pressed.
    """

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
        """Used to know if a button is held."""
        return bool(self.value)

    @property
    def hold_time(self) -> float:
        """Returns the time an event has been held."""
        return 0 if self.time is None else time.time() - self.time

    def __repr__(self) -> str:
        return f"PlayerInput<{self.key}, {self.pressed}, {self.released}, {self.triggered}, {self.value}, {self.hold_time}>"


class EventStore(dict[int, Event]):
    """Manage events handled by event handlers."""

    def __missing__(self, key) -> Event:
        self[key] = Event(key)
        return self[key]

    def __iter__(self) -> Iterator[Event]:
        return iter(self.values())

    def flush(self) -> None:
        """Remove all events from the store. Used between state change."""
        self.clear()
