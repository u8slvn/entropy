from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.game.states.story.factory import build_event
from entropy.game.states.story.node import Node
from entropy.tools.timer import TimerSecond


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
        event: dict[str, str],
        background: str,
        delay: int = 0,
        music: str | None = None,
        transition: dict[str, str] | None = None,
        **_,
    ):
        super().__init__(chapter=chapter, next=next)
        self._id = id
        self._music = music
        self._transition = transition
        self.chapter.set_background(config=background)
        self._event = build_event(parent=self.chapter.background, config=event)
        self._delay = TimerSecond(duration=delay, callback=self._event.setup)

    def setup(self) -> None:
        super().setup()
        self._delay.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        if self._delay.is_done():
            print(self._event)
            self._event.update()
        else:
            self._delay.update()

    def draw(self, surface: pygame.Surface) -> None:
        if self._delay.is_done():
            self._event.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._delay.teardown()
        self._event.teardown()
