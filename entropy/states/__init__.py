from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Type


if TYPE_CHECKING:
    import pygame as pg

    from entropy.misc.control import Control

__all__ = ["State", "States"]


class States:
    @classmethod
    def load(cls) -> dict[str, State]:
        # TODO: add auto load
        from entropy.states.splash import Splash  # noqa
        from entropy.states.title_screen import TitleScreen  # noqa

        return {name.upper(): state() for name, state in State.states.items()}


class State(ABC):
    states: dict[str, Type[State]] = {}

    def __init__(self) -> None:
        self.control: Control | None = None

    def __init_subclass__(cls, **kwargs) -> None:
        State.states[cls.__name__] = cls

    def startup(self, control: Control) -> None:
        self.control = control

    def cleanup(self) -> None:
        self.control = None

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        ...
