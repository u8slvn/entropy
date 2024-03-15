from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Type

import pygame

from entropy.game.entity import GameEntity
from entropy.gui.elements.base import UIElementGroup
from entropy.logging import get_logger


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control

logger = get_logger()


class State(GameEntity, ABC):
    _states: ClassVar[dict[str, Type[State]]] = {}

    def __init__(self, control: Control) -> None:
        self.ui_elements = UIElementGroup()
        self.control = control

    def __init_subclass__(cls) -> None:
        State._states[cls.get_name()] = cls

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_states(cls) -> dict[str, Type[State]]:
        return cls._states

    def transition_to(self, state_name: str, with_exit: bool = False) -> None:
        self.control.transition_to(state_name=state_name, with_exit=with_exit)

    def process_event(self, event: Event) -> None:
        self.ui_elements.process_event(event)

    def update(self, dt: float) -> None:
        self.ui_elements.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self.ui_elements.draw(surface)

    def teardown(self) -> None:
        pass
        # self.control.event_manager.flush()

    def exit(self) -> None:
        self.ui_elements.cleanup()
        self.teardown()
        self.control.state_stack.pop()
        self.control.current_state.setup()
        logger.info(f'Game state changed to "{self.control.current_state.get_name()}".')

    def __repr__(self) -> str:
        return f"State<{self.get_name()}>"
