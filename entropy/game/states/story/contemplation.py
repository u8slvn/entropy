from __future__ import annotations

from typing import TYPE_CHECKING

from entropy.game.states.story.factory import build_event
from entropy.game.states.story.node import Node
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.image import Image
from entropy.tools.timer import TimerSecond
from entropy.utils import Pos


if TYPE_CHECKING:
    from pygame import pygame

    from entropy.game.states.story import Chapter
    from entropy.gui.input import Inputs


class ContemplationScene(Node):
    def __init__(
        self,
        chapter: Chapter,
        id: str,
        next_id: str,
        event: dict[str, str],
        delay: int = 0,
        background: str | None = None,
        music: str | None = None,
        ease_in: dict[str, str | int] | None = None,
        ease_out: dict[str, str | int] | None = None,
        **_,
    ):
        super().__init__(
            chapter=chapter,
            next_id=next_id,
            music=music,
            background=background,
            ease_in=ease_in,
            ease_out=ease_out,
        )
        self._id = id
        self._event_store = build_event(parent=self.chapter.background, params=event)
        self._event = next(self._event_store)
        self._background_event = Image(
            parent=self.chapter.background,
            name="contemplation-text-bg-a",
            pos=Pos(0, 672),
            align=Align.CENTER_X,
        )
        self._delay = TimerSecond(duration=delay)

    def setup(self) -> None:
        super().setup()
        self._delay.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE or inputs.keyboard.ENTER or inputs.mouse.BUTTON1:
            if not self._delay.is_done():
                self._delay.stop()
            elif self._event.is_done():
                try:
                    self._event = next(self._event_store)
                except StopIteration:
                    self.close()
            else:
                self._event.skip()

    def update(self, dt: float) -> None:
        super().update(dt=dt)
        if self._delay.is_done():
            self._event.update(dt=dt)
        else:
            self._delay.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._background_event.draw(surface=surface)
        if self._delay.is_done():
            self._event.draw(surface=surface)
        super().draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._delay.teardown()
        self._event.teardown()
