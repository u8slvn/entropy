from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import pygame as pg

from entropy import assets
from entropy.event.specs import a_or_click_is_pressed
from entropy.game.states._story.node.base import Node
from entropy.gui.elements.text import Text
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.tools.timer import TimerSecond


if TYPE_CHECKING:
    from entropy.event.event import Event
    from entropy.game.states._story.chapter import Chapter


class IntroScene(Node):
    def __init__(
        self,
        chapter: Chapter,
        id: str,
        next_id: str,
        music: str,
        title: str,
        subtitle: str,
        background: str,
        **_: dict[str, Any],
    ) -> None:
        super().__init__(
            chapter=chapter, next_id=next_id, music=music, background=background
        )
        self._id = id
        self._title = Text(
            chapter.ui_elements,
            font=assets.font.get("LanaPixel", "xxxl"),
            text=title,
            color=pg.Color("white"),
            center=(chapter.background.rect.centerx, 400),
        )
        self._subtitle = Text(
            chapter.ui_elements,
            font=assets.font.get("LanaPixel", "md"),
            text=subtitle,
            color=pg.Color("white"),
            center=(chapter.background.rect.centerx, 550),
        )
        self._fade_out = FadeOut(duration=3000, callback=self.mark_as_done)
        self._timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=2000, callback=self._timer.start)

    def setup(self) -> None:
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_event(self, event: Event) -> None:
        if a_or_click_is_pressed(event):
            self.mark_as_done()

    def update(self, dt: float) -> None:
        self._fade_in.update(dt=dt)
        self._fade_out.update(dt=dt)
        self._timer.update(dt=dt)

    def draw(self, surface: pg.Surface) -> None:
        super().draw(surface)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
