from __future__ import annotations

import json

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.game.states.story.contemplation import ContemplationScene
from entropy.game.states.story.node import BaseNode
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.base import ALIGN
from entropy.gui.widgets.text import TText
from entropy.locations import STORY_DIR
from entropy.logging import get_logger
from entropy.tools.timer import TimerSecond
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.states.base import State
    from entropy.gui.input import Inputs

logger = get_logger()

NODE_TYPE_MAPPING = {
    "contemplation": ContemplationScene,
}


class Chapter(BaseNode):
    def __init__(
        self, state: State, title: str, subtitle: str, start_node: str, configfile: Path
    ) -> None:
        super().__init__()
        self._name = title
        self._state = state
        self._current_node_id = start_node
        self._nodes: dict[str, BaseNode] = {}
        self._load_nodes(configfile=configfile)
        self._loaded = False

        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._title = TText(
            parent=self._background,
            font=entropy.assets.fonts.get("LanaPixel", "chapter"),
            text=title,
            color="white",
            pos=Pos(0, 400),
            align=ALIGN.CENTER_X,
        )
        self._subtitle = TText(
            parent=self._background,
            font=entropy.assets.fonts.get("LanaPixel", "big"),
            text=subtitle,
            color="white",
            pos=Pos(0, 550),
            align=ALIGN.CENTER_X,
        )
        self._fade_out = FadeOut(duration=3000, callback=self.mark_as_loaded)
        self._timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=2000, callback=self._timer.start)

    def _load_nodes(self, configfile: Path) -> None:
        with open(STORY_DIR / configfile, "r") as file:
            nodes = json.load(file)

        for node in nodes:
            self._nodes[node["id"]] = NODE_TYPE_MAPPING[node["type"]](
                chapter=self, **node
            )

    @property
    def current_node(self) -> BaseNode:
        return self._nodes[self._current_node_id]

    def mark_as_loaded(self) -> None:
        logger.debug(f'Chapter "{self._name}" loaded.')
        self._loaded = True
        self.current_node.setup()

    def transition_to_node(self, id_: str) -> None:
        if id_ == "end":
            logger.debug(f'Chapter "{self._name}" ended.')
            self.mark_as_done()
        else:
            logger.debug(f'Chapter "{self._name}" transition to node "{id_}".')
            self._current_node_id = id_

    def setup(self) -> None:
        super().setup()
        self._title.setup()
        self._subtitle.setup()
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self.current_node.process_inputs(inputs=inputs)

    def update(self) -> None:
        if self._loaded is False:
            self._title.update()
            self._subtitle.update()
            self._fade_in.update()
            self._fade_out.update()
            self._timer.update()
        else:
            if self.current_node.is_done():
                self._current_node_id = self.current_node
            self.current_node.update()

    def draw(self, surface: pygame.Surface) -> None:
        if self._loaded is False:
            self._background.draw(surface=surface)
            self._title.draw(surface=surface)
            self._subtitle.draw(surface=surface)
            self._fade_out.draw(surface=surface)
            self._fade_in.draw(surface=surface)
        else:
            self.current_node.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
        self.current_node.teardown()
