from __future__ import annotations

import json

from functools import partial
from typing import TYPE_CHECKING
from typing import Callable
from typing import Type

import pygame

from entropy.game.states.story.factory import build_background
from entropy.game.states.story.node.base import BaseNode
from entropy.game.states.story.node.base import NullNode
from entropy.game.states.story.node.contemplation import ContemplationScene
from entropy.game.states.story.node.intro import IntroScene
from entropy.gui.elements.background import ColorBackground
from entropy.locations import STORY_DIR
from entropy.logging import get_logger
from entropy.utils.measure import Color
from entropy.utils.measure import cleanup


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.states.base import State
    from entropy.game.states.story.node.base import Node
    from entropy.gui.elements.background import Background

logger = get_logger()

NODE_TYPE_MAPPING: dict[str, Type[Node]] = {
    "contemplation": ContemplationScene,
    "intro": IntroScene,
}


class Chapter(BaseNode):
    """Chapter class.
    Represent a Chapter of the game and handle all the nodes of a chapter of the game.
    """

    def __init__(
        self, state: State, name: str, start_node: str, configfile: str
    ) -> None:
        super().__init__()
        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._name = name
        self._state = state
        self.ui_elements = self._state.ui_elements
        self._nodes: dict[str, Callable[[], Node]] = {}
        self._current_node: Node = NullNode(chapter=self)
        self._loaded = False

        self._load_nodes(configfile=configfile)
        self.transition_to_node(uuid=start_node)

    def _load_nodes(self, configfile: str) -> None:
        """Load all the Story Nodes from the given JSON config file."""
        # TODO: add in thread with loading screen
        with open(STORY_DIR / configfile, "r") as file:
            nodes = json.load(file)

        for node in nodes:
            self._nodes[node["id"]] = partial(
                NODE_TYPE_MAPPING[node["type"]],
                chapter=self,
                **node,
            )

    def _build_node(self, uuid: str) -> Node:
        """Build a story node from the given uuid."""
        try:
            node = self._nodes[uuid]
        except KeyError:
            raise ValueError(f'Node with uuid "{uuid}" does not exit.')

        return node()

    def _get_next_node_uuid(self) -> str:
        """Return the next node uuid."""
        if self._current_node is None:
            # End the Chapter if there is no Node currently loaded in it.
            return "end"

        return self._current_node.next_id

    @property
    def background(self) -> Background:
        """Expose the background of the Chapter as it may be used as root widget
        for the nodes.
        """
        return self._background

    def set_background(self, config: str | None) -> None:
        """Set the Chapter's background.
        Used by the Story Nodes to set the background of the Chapter.
        """
        if config is not None:
            self._background = build_background(params=config)

    def transition_to_node(self, uuid: str) -> None:
        """Transition from the Chapter current node to the one with the given uuid."""
        if uuid == "end":  # "end" uuid indicate the end of the chapter.
            logger.debug(f'Chapter "{self._name}" ended.')
            self.mark_as_done()
            return

        if self._current_node is not None:
            # Avoid teardown with the first node transition.
            self._current_node.teardown()
            cleanup(self._current_node)

        self._current_node = self._build_node(uuid=uuid)
        self._current_node.setup()
        logger.debug(f'Chapter "{self._name}" transition to node "{uuid}".')

    def setup(self) -> None:
        """Set up the Chapter."""
        super().setup()

    def process_event(self, event: Event) -> None:
        """Process game inputs."""
        self._current_node.process_event(event=event)

    def update(self, dt: float) -> None:
        """Update the Chapter within the game loop."""
        self._current_node.update(dt=dt)

        if self._current_node.is_done():
            # Transition to next node
            next_node_uuid = self._get_next_node_uuid()
            self.transition_to_node(uuid=next_node_uuid)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw method of the Chapter.
        Always draws the background first then the current node.
        """
        self._background.draw(surface=surface)
        self._current_node.draw(surface=surface)

    def teardown(self) -> None:
        """Teardown the Chapter."""
        super().teardown()
        self._current_node.teardown()
