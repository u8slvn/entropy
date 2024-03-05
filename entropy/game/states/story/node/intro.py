from __future__ import annotations

from typing import TYPE_CHECKING

from entropy import assets
from entropy.game.states.story.node.base import Node
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TText
from entropy.tools.timer import TimerSecond
from entropy.utils import Pos


if TYPE_CHECKING:
    import pygame

    from entropy.game.states.story import Chapter
    from entropy.gui.input import Inputs


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
        **_,
    ):
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

    def process_inputs(self, inputs: Inputs) -> None:
        if inputs.keyboard.SPACE or inputs.keyboard.ENTER or inputs.mouse.BUTTON1:
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