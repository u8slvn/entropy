from __future__ import annotations


A = 10
B = 11

UP = 20
RIGHT = 21
LEFT = 22
DOWN = 23

SELECT = 30
START = 31


class KeyMap(dict):
    def __init__(
        self,
        a: int | None = None,
        b: int | None = None,
        up: int | None = None,
        right: int | None = None,
        left: int | None = None,
        down: int | None = None,
        start: int | None = None,
        select: int | None = None,
    ):
        mapping = {
            A: a,
            B: b,
            UP: up,
            RIGHT: right,
            LEFT: left,
            DOWN: down,
            SELECT: select,
            START: start,
        }
        mapping = {event: key for key, event in mapping.items() if event is not None}
        super().__init__(mapping)
