from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from entropy.game.story.nodes.base import Node


if TYPE_CHECKING:
    import pygame as pg

    from entropy.game.story.nodes.base import Audio
    from entropy.gui.elements.background import Background
    from entropy.gui.elements.text import Text
    from entropy.gui.transistions.base import Transition


class IntroNode(Node):
    """IntroNode class.
    Intro node is the first node of a chapter, and it displays the title and the
    subtitle of the chapter.
    """

    def __init__(
        self,
        uuid: str,
        next_uuid: str,
        background: Background,
        audio: Audio,
        attributes: dict[str, Any],
    ) -> None:
        super().__init__(uuid, next_uuid, background, audio)
        self.check_attributes(attributes)
        self.title: Text = attributes["title"]
        self.subtitle: Text = attributes["subtitle"]
        self.ease_in: Transition = attributes["ease_in"]
        self.ease_out: Transition = attributes["ease_out"]

    def update(self, dt: float) -> None:
        self.ease_in.update(dt)
        self.ease_out.update(dt)

    def draw(self, surface: pg.Surface) -> None:
        self.title.draw(surface)
        self.subtitle.draw(surface)
        self.ease_in.draw(surface)
        self.ease_out.draw(surface)
