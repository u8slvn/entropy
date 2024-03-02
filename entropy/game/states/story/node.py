from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from entropy.game.entity import GameEntity


if TYPE_CHECKING:
    from entropy.game.states.base import State
    from entropy.gui.input import Inputs


class BaseNode(GameEntity):

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass


class Chapter(BaseNode):
    def __init__(
        self, state: State, title: str, subtitle: str, start_node: str, configfile: Path
    ) -> None:
        self._state = state
        self._title = title
        self._subtitle = subtitle
        self._start_node = start_node
        self._nodes: dict[str, Node] = {}
        self._load(configfile=configfile)

    # self._background = ColorBackground(color=Color(0, 0, 0, 255))
    def _load(self, configfile: Path) -> None: ...

    def setup(self) -> None: ...

    def process_inputs(self, inputs: Inputs) -> None: ...

    def update(self) -> None: ...

    def draw(self, surface: pygame.Surface) -> None: ...

    def teardown(self) -> None: ...


class Node(BaseNode):
    pass
