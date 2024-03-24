from collections import deque
from typing import Any


class NodeEvent:
    def __init__(self):
        self.done = False

    def process_event(self, event: Event) -> None:
    def update(self, dt: float) -> None:
        pass


class NodeEvents:
    def __init__(self, events: list[NodeEvent]) -> None:
        self._events = deque(events)

    def next(self) -> NodeEvent | None:
        try:
            return self._events.popleft()
        except IndexError:
            return None

