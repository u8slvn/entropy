from __future__ import annotations

import time

from abc import ABC
from abc import abstractmethod
from types import MappingProxyType
from typing import Any
from typing import Generator
from typing import Iterator

import pygame as pg

from entropy.event.types import input
from entropy.event.types import system


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


class EventQueueHandler:
    def __init__(self):
        self._event_handlers: list[EventHandler] = [
            SystemEventHandler(),
            KeyboardEventHandler(),
            MouseEventHandler(),
        ]

    def process_events(self) -> Generator[Event, None, None]:
        for event in pg.event.get():
            for event_handler in self._event_handlers:
                event_handler.process_event(event=event)

        for event_handler in self._event_handlers:
            yield from event_handler.get_events()


class EventHandler(ABC):
    default_mapping: EventMapping

    def __init__(self, keymap: EventMapping | None = None):
        self._mapping = keymap or self.default_mapping
        self._event_store = EventStore()

    @abstractmethod
    def process_event(self, event: pg.event.Event) -> None:
        raise NotImplementedError

    def get_events(self) -> Generator[Event, None, None]:
        for event in self._event_store:
            if event.triggered:
                yield event
                event.value = 0
                event.triggered = False
            elif event.pressed:
                yield event
                event.pressed = False
            elif event.held:
                yield event
            elif event.released:
                yield event
                event.released = False

    def press(self, key: int, value: int | tuple[int, int] = 1) -> None:
        self._event_store[key].value = value
        self._event_store[key].pressed = True
        self._event_store[key].time = time.time()

    def release(self, key: int) -> None:
        self._event_store[key].value = 0
        self._event_store[key].released = True
        self._event_store[key].time = None

    def trigger(self, key: int, value: int | tuple[int, int] = 1) -> None:
        self._event_store[key].value = value
        self._event_store[key].triggered = True


class SystemEventHandler(EventHandler):
    default_mapping = EventMapping(
        {
            pg.QUIT: system.QUIT,
            pg.VIDEORESIZE: system.DISPLAY_RESIZE,
        }
    )

    def process_event(self, event: pg.event.Event) -> None:
        if key := self._mapping.get(event.type):
            if event.type == pg.VIDEORESIZE:
                self.trigger(key, value=event.size)
            else:
                self.trigger(key)


class MouseEventHandler(EventHandler):
    default_mapping = EventMapping(
        {
            pg.MOUSEBUTTONUP: input.CLICK,
            pg.MOUSEBUTTONDOWN: input.CLICK,
            pg.MOUSEMOTION: input.MOVE,
        }
    )

    def process_event(self, event: pg.event.Event) -> None:
        if key := self._mapping.get(event.type):
            if event.type == pg.MOUSEBUTTONDOWN:
                self.press(key, value=event.pos)
            elif event.type == pg.MOUSEBUTTONUP:
                self.release(key)
            elif event.type == pg.MOUSEMOTION:
                self.trigger(key, value=event.pos)


class KeyboardEventHandler(EventHandler):
    default_mapping = EventMapping(
        {
            pg.K_SPACE: input.A,
            pg.K_RETURN: input.B,
            pg.K_UP: input.UP,
            pg.K_RIGHT: input.RIGHT,
            pg.K_LEFT: input.LEFT,
            pg.K_DOWN: input.DOWN,
            pg.K_ESCAPE: input.BACK,
            pg.K_F5: input.DEBUG,
        }
    )

    def process_event(self, event: pg.event.Event) -> None:
        pressed = event.type == pg.KEYDOWN
        released = event.type == pg.KEYUP
        if pressed or released:
            if key := self._mapping.get(event.key):
                if pressed:
                    self.press(key)
                else:
                    self.release(key)
