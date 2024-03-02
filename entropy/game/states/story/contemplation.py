from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.game.states.story.factory import build_background
from entropy.game.states.story.node import Node


if TYPE_CHECKING:
    from pygame import pygame

    from entropy.game.states.story import Chapter
    from entropy.gui.input import Inputs


class ContemplationScene(Node):
    def __init__(
        self,
        chapter: Chapter,
        id: str,
        next: str,
        music: str,
        transition: dict[str, str],
        events: list[dict[str, str]],
        background: str,
        **_,
    ):
        super().__init__(chapter=chapter, next=next)
        self._id = id
        self._music = music
        self._transition = transition
        self._events = events
        self._background = build_background(config=background)

    def setup(self) -> None:
        super().setup()

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
