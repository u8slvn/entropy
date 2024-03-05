from __future__ import annotations

import time

from typing import Any
from typing import Generator

import pygame as pg

from entropy.events.keys import KeyMap


# if TYPE_CHECKING:


default_keymap = KeyMap(
    a=pg.K_SPACE,
    b=pg.K_RETURN,
    up=pg.K_UP,
    right=pg.K_RIGHT,
    left=pg.K_LEFT,
    down=pg.K_DOWN,
    start=pg.K_ESCAPE,
    select=pg.K_BACKSPACE,
)


class PlayerInput:
    __slots__ = ("key", "value", "pressed", "released", "time")

    def __init__(self, key: int, value: Any = 1):
        self.key = key
        self.value = value
        self.pressed = False
        self.released = False
        self.time = None

    @property
    def held(self) -> bool:
        return bool(self.value)

    @property
    def hold_time(self) -> float:
        return 0 if self.time is None else time.time() - self.time

    def __repr__(self) -> str:
        return f"PlayerInput<{self.key}, {self.pressed}, {self.released}, {self.value}, {self.hold_time}>"


class EventStore(dict[str, PlayerInput]):
    def __missing__(self, key):
        self[key] = PlayerInput(key)
        return self[key]

    @property
    def events(self) -> Generator[PlayerInput, None, None]:
        for event in self.values():
            if event.pressed:
                yield event
                event.pressed = False
            elif event.held:
                yield event
            elif event.released:
                yield event
                event.released = False


class EventHandler:
    def __init__(self, keymap: KeyMap = default_keymap):
        self._keymap = keymap
        self._event_store = EventStore()

    def process_event(self, event: pg.event.Event) -> None:
        pressed = event.type == pg.KEYDOWN
        released = event.type == pg.KEYUP
        if pressed or released:
            if key := self._keymap.get(event.key):

                if pressed:
                    self._event_store[key].value = 1
                    self._event_store[key].pressed = True
                    self._event_store[key].time = time.time()
                else:
                    self._event_store[key].value = 0
                    self._event_store[key].released = True
                    self._event_store[key].time = None

    def get_events(self) -> Generator[PlayerInput, None, None]:
        yield from self._event_store.events
