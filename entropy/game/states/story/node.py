from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pygame

import entropy

from entropy.game.entity import GameEntity
from entropy.gui.transistions.fader import FadeIn
from entropy.gui.transistions.fader import FadeOut
from entropy.gui.widgets.background import ColorBackground
from entropy.gui.widgets.base import ALIGN
from entropy.gui.widgets.text import TText
from entropy.logging import get_logger
from entropy.tools.timer import TimerSecond
from entropy.utils import Color
from entropy.utils import Pos


if TYPE_CHECKING:
    from entropy.game.states.base import State
    from entropy.gui.input import Inputs


logger = get_logger()


class BaseNode(GameEntity):

    def setup(self) -> None:
        pass

    def process_inputs(self, inputs: Inputs) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass


class Chapter(BaseNode):
    def __init__(
        self, state: State, title: str, subtitle: str, start_node: str, configfile: Path
    ) -> None:
        self._name = title
        self._state = state
        self._start_node = start_node
        self._nodes: dict[str, Node] = {}
        self._load(configfile=configfile)
        self._loaded = False
        self._done = False

        self._background = ColorBackground(color=Color(0, 0, 0, 255))
        self._title = TText(
            parent=self._background,
            font=entropy.assets.fonts.get("LanaPixel", "chapter"),
            text=title,
            color="white",
            pos=Pos(0, 400),
            align=ALIGN.CENTER_X,
        )
        self._subtitle = TText(
            parent=self._background,
            font=entropy.assets.fonts.get("LanaPixel", "big"),
            text=subtitle,
            color="white",
            pos=Pos(0, 550),
            align=ALIGN.CENTER_X,
        )
        self._fade_out = FadeOut(duration=3000, callback=self.mark_as_loaded)
        self._timer = TimerSecond(
            duration=1,
            autostart=False,
            callback=self._fade_out.activate,
        )
        self._fade_in = FadeIn(duration=3000, callback=self._timer.start)

    def _load(self, configfile: Path) -> None: ...

    def mark_as_loaded(self) -> None:
        logger.debug(f'Chapter "{self._name}" loaded.')
        self._loaded = True

    def setup(self) -> None:
        self._title.setup()
        self._subtitle.setup()
        self._fade_in.setup()
        self._fade_out.setup()
        self._timer.setup()

    def process_inputs(self, inputs: Inputs) -> None: ...

    def update(self) -> None:
        self._title.update()
        self._subtitle.update()
        self._fade_in.update()
        self._fade_out.update()
        self._timer.update()

    def draw(self, surface: pygame.Surface) -> None:
        self._background.draw(surface=surface)
        self._title.draw(surface=surface)
        self._subtitle.draw(surface=surface)
        self._fade_out.draw(surface=surface)
        self._fade_in.draw(surface=surface)

    def teardown(self) -> None:
        self._done = False
        self._fade_out.teardown()
        self._fade_in.teardown()
        self._timer.teardown()


class Node(BaseNode):
    pass
