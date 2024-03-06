from __future__ import annotations

import time

from abc import ABC
from abc import abstractmethod
from typing import Generator

import pygame as pg

from entropy.event.event import Event
from entropy.event.event import EventMapping
from entropy.event.event import EventStore
from entropy.event.types import inputs
from entropy.event.types import system


class EventQueueHandler:
    def __init__(self):
        self._event_handlers: list[EventHandler] = [
            SystemEventHandler(),
            # Order is very important, Mouse should always be handled before keyboard,
            # in order to manage its visibility.
            MouseEventHandler(),
            KeyboardEventHandler(),
        ]

    def process_events(self) -> Generator[Event, None, None]:
        for event in pg.event.get():
            for event_handler in self._event_handlers:
                event_handler.process_event(event=event)

        for event_handler in self._event_handlers:
            yield from event_handler.get_events()

    def flush(self) -> None:
        for event_handler in self._event_handlers:
            event_handler.flush()


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

    def flush(self) -> None:
        self._event_store.flush()

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
            pg.MOUSEBUTTONUP: inputs.CLICK,
            pg.MOUSEBUTTONDOWN: inputs.CLICK,
            pg.MOUSEMOTION: inputs.MOVE,
            pg.KEYDOWN: system.HIDE_MOUSE,
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
            elif event.type == pg.KEYDOWN:
                self.trigger(key)


class KeyboardEventHandler(EventHandler):
    default_mapping = EventMapping(
        {
            pg.K_SPACE: inputs.A,
            pg.K_RETURN: inputs.B,
            pg.K_UP: inputs.UP,
            pg.K_RIGHT: inputs.RIGHT,
            pg.K_LEFT: inputs.LEFT,
            pg.K_DOWN: inputs.DOWN,
            pg.K_ESCAPE: inputs.BACK,
            pg.K_F5: inputs.DEBUG,
            pg.K_F6: inputs.FULLSCREEN,
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
