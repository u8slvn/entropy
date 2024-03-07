from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from entropy import assets
from entropy.event.types import inputs
from entropy.game.states.story.node.base import Node
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TText
from entropy.tools.timer import TimerSecond
from entropy.utils.measure import Pos


if TYPE_CHECKING:
    import pygame

    from entropy.event.event import Event
    from entropy.game.states.story.chapter import Chapter


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
        self._title = TText(
            parent=self.chapter.background,
            font=assets.font.get("LanaPixel", "chapter"),
            text=title,
            color="white",
            pos=Pos(0, 400),
            align=Align.CENTER_X,
        )
        self._subtitle = TText(
            parent=self.chapter.background,
            font=assets.font.get("LanaPixel", "big"),
            text=subtitle,
            color="white",
            pos=Pos(0, 550),
            align=Align.CENTER_X,
        )
        self._fade_out = FadeOut(duration=3000, callback=self.mark_as_done)
        self._timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=2000, callback=self._timer.start)

    def setup(self) -> None:
        super().setup()
        self._title.setup()
        self._subtitle.setup()
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_event(self, event: Event) -> None:
        if event.pressed and event.key in (inputs.CLICK, inputs.A):
            self.mark_as_done()

    def update(self, dt: float) -> None:
        self._title.update(dt=dt)
        self._subtitle.update(dt=dt)
        self._fade_in.update(dt=dt)
        self._fade_out.update(dt=dt)
        self._timer.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._title.draw(surface=surface)
        self._subtitle.draw(surface=surface)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        super().teardown()
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()
