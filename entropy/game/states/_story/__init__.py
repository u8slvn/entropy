from __future__ import annotations

import json

from typing import TYPE_CHECKING
from typing import Any
from typing import cast

import pygame

from entropy import translator
from entropy.config import get_config
from entropy.game.states._story.chapter import Chapter
from entropy.locations import STORY_DIR
from entropy.logging import get_logger


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.control import Control

config = get_config()
logger = get_logger()


class Story:
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._chapters = self._load_chapters()

        # TODO: get default slot save.
        self._set_chapter("chapter01")

    @staticmethod
    def _load_chapters() -> dict[str, dict[str, str]]:
        with open(STORY_DIR / "main.json", "r") as file:
            return cast(dict[str, Any], json.load(file))

    def _set_chapter(self, name: str) -> None:
        logger.info(f'Story chapter set to "{name}".')
        translator.set_translation(locale=config.locale, domain=name)
        self._current_chapter = Chapter(state=self, name=name, **(self._chapters[name]))

    def setup(self) -> None:
        self._current_chapter.setup()

    def process_event(self, event: Event) -> None:
        self._current_chapter.process_event(event)

    def update(self, dt: float) -> None:
        if self._current_chapter.is_done():
            self.exit()
        self._current_chapter.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._current_chapter.draw(surface=surface)

    def teardown(self) -> None:
        self._current_chapter.teardown()
