from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from entropy.event.specs import a_or_click_is_pressed
from entropy.game.states._story.factory import build_event
from entropy.game.states._story.node.base import Node
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.image import Image
from entropy.tools.timer import TimerSecond
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    import pygame

    from entropy.event.event import Event
    from entropy.game.states._story.chapter import Chapter


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
        **_: dict[str, Any],
    ) -> None:
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

    def process_event(self, event: Event) -> None:
        if a_or_click_is_pressed(event):
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
