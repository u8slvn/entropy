from __future__ import annotations

from typing import TYPE_CHECKING

import entropy

from entropy.game.states.story.node import Node
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.base import Align
from entropy.gui.widgets.text import TText
from entropy.tools.timer import TimerSecond
from entropy.utils import Pos


if TYPE_CHECKING:
    from pygame import pygame

    from entropy.game.states.story import Chapter
    from entropy.gui.input import Inputs


class IntroScene(Node):
    def __init__(
        self,
        chapter: Chapter,
        id: str,
        next: str,
        music: str,
        title: str,
        subtitle: str,
        background: str,
        **_,
    ):
        super().__init__(chapter=chapter, next=next)
        self._id = id
        self._music = music
        self.chapter.set_background(config=background)
        self._title = TText(
            parent=self.chapter.background,
            font=entropy.assets.fonts.get("LanaPixel", "chapter"),
            text=title,
            color="white",
            pos=Pos(0, 400),
            align=Align.CENTER_X,
        )
        self._subtitle = TText(
            parent=self.chapter.background,
            font=entropy.assets.fonts.get("LanaPixel", "big"),
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

    def mark_as_done(self) -> None:
        super().mark_as_done()
        self.transition_to_next()

    def setup(self) -> None:
        super().setup()
        self._title.setup()
        self._subtitle.setup()
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        self._title.update()
        self._subtitle.update()
        self._fade_in.update()
        self._fade_out.update()
        self._timer.update()

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
