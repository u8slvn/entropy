from __future__ import annotations

import json

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Callable
from typing import Type

import pygame

from entropy.game.states.story.contemplation import ContemplationScene
from entropy.game.states.story.factory import build_background
from entropy.game.states.story.intro import IntroScene
from entropy.game.states.story.node import BaseNode
from entropy.gui.widgets.background import ColorBackground
from entropy.locations import STORY_DIR
from entropy.logging import get_logger
from entropy.utils import Color
from entropy.utils import cleanup


if TYPE_CHECKING:
    from entropy.game.states.base import State
    from entropy.game.states.story.node import Node
    from entropy.gui.input import Inputs
    from entropy.gui.widgets.background import Background

logger = get_logger()

NODE_TYPE_MAPPING: dict[str, Type[Node]] = {
    "contemplation": ContemplationScene,
    "intro": IntroScene,
}


class Chapter(BaseNode):
    def __init__(
        self, state: State, name: str, start_node: str, configfile: Path
    ) -> None:
        super().__init__()
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._name = name
        self._state = state
        self._nodes: dict[str, Callable[[], None]] = {}
        self._load_nodes(configfile=configfile)
        self._current_node: Node | None = None
        self.transition_to_node(id=start_node)
        self._loaded = False

    def _load_nodes(self, configfile: Path) -> None:
        with open(STORY_DIR / configfile, "r") as file:
            nodes = json.load(file)

        for node in nodes:
            self._nodes[node["id"]] = partial(
                NODE_TYPE_MAPPING[node["type"]],
                chapter=self,
                **node,
            )

    @property
    def background(self) -> Background:
        return self._background

    def set_background(self, config: str | None) -> None:
        if config is not None:
            self._background = build_background(params=config)

    def transition_to_node(self, id: str) -> None:
        if id == "end":
            logger.debug(f'Chapter "{self._name}" ended.')
            self.mark_as_done()
            return

        if self._current_node is not None:
            self._current_node.teardown()
            cleanup(self._current_node)

        self._current_node = self._nodes[id]()
        self._current_node.setup()
        logger.debug(f'Chapter "{self._name}" transition to node "{id}".')

    def setup(self) -> None:
        super().setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._current_node.process_inputs(inputs=inputs)

    def update(self, dt: float) -> None:
        self._current_node.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)
        self._current_node.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._current_node.teardown()
