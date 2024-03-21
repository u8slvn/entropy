from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from entropy import translator
from entropy import window
from entropy.config import get_config
from entropy.game.states.base import State
from entropy.game.story.chapter import ChapterCollection
from entropy.game.story.chapter import NullChapter
from entropy.game.story.nodes.base import NullNode
from entropy.locations import STORY_DIR
from entropy.logging import get_logger


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control
    from entropy.game.story.chapter import Chapter
    from entropy.game.story.nodes.base import Node

config = get_config()
logger = get_logger()


class Story(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._chapters = ChapterCollection(dir_path=STORY_DIR, index_file="index")
        self._current_chapter: Chapter = NullChapter()
        self._current_node: Node = NullNode()
        self.set_chapter(name="chapter01")
        self._background = pygame.Surface(window.default_res)

    def set_chapter(self, name: str) -> None:
        logger.info(f'Story chapter set to "{name}".')
        translator.set_translation(locale=config.locale, domain=name)
        self._current_chapter = self._chapters.load_chapter(name="chapter01")
        self._current_node = self._current_chapter.get_node()

    def setup(self) -> None:
        self._current_node.setup()

    def process_event(self, event: Event) -> None:
        self._current_node.process_event(event)

    def update(self, dt: float) -> None:
        if self._current_node.done:
            self.exit()
        self._current_node.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._current_node.draw(surface=surface)

    def teardown(self) -> None:
        self._current_node.teardown()
