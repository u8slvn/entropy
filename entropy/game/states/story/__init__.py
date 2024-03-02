from __future__ import annotations

import json

from typing import TYPE_CHECKING

import pygame

from entropy import config
from entropy import get_logger
from entropy import translator
from entropy.game.states.base import State
from entropy.game.states.story.chapter import Chapter
from entropy.locations import STORY_DIR


if TYPE_CHECKING:
    from entropy.game.control import Control
    from entropy.gui.input import Inputs

logger = get_logger()


class Story(State):
    def __init__(self, control: Control) -> None:
        super().__init__(control=control)
        self._chapters = self._load_chapters()

        # TODO: get default slot save.
        self._set_chapter("chapter01")

    def _load_chapters(self) -> dict[str, dict[str, str]]:
        with open(STORY_DIR / "main.json", "r") as file:
            return json.load(file)

    def _set_chapter(self, name: str) -> None:
        logger.info(f'Story chapter set to "{name}".')
        translator.set_translation(locale=config.locale, domain=name)
        self._current_chapter = Chapter(state=self, **(self._chapters[name]))

    def setup(self) -> None:
        self._current_chapter.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        self._current_chapter.process_inputs(inputs)

    def update(self) -> None:
        self._current_chapter.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._current_chapter.draw(surface=surface)

    def teardown(self) -> None:
        self._current_chapter.teardown()


# self._text = TypeWriterText(
#     parent=self._background,
#     font=font,
#     text="Gamer Barbany était un prodige des mondes virtuels, où il régnait en maître. Mais son plus grand défi l'attendait dans la réalité, où il trouva l'amour, dépassant ainsi les limites de son écran pour découvrir un univers bien plus vaste et profond.",
#     color="white",
#     width=600,
#     speed=1.4,
#     align=ALIGN.CENTER,
# )
