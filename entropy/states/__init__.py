from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Type


if TYPE_CHECKING:
    import pygame as pg

    from entropy.misc.action import Actions
    from entropy.misc.control import Control
    from entropy.misc.mouse import Mouse

__all__ = ["State", "load_states"]


def load_states() -> dict[str, Type[State]]:
    # TODO: add auto load
    from entropy.states.splash import Splash  # noqa
    from entropy.states.title_screen import TitleScreen  # noqa

    return State.states


class State(ABC):
    states: dict[str, Type[State]] = {}

    def __init__(self, control: Control) -> None:
        self.control = control

    def __init_subclass__(cls, **kwargs) -> None:
        State.states[cls.__name__.upper()] = cls

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, actions: Actions, mouse: Mouse) -> None:
        ...

    @abstractmethod
    def draw(self, surface: pg.Surface) -> None:
        ...
