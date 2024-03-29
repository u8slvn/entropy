from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar

from entropy import mixer
from entropy.event.event import Event
from entropy.game.entity import GameEntity
from entropy.logging import get_logger


if TYPE_CHECKING:
    import pygame as pg

    from entropy.gui.elements.background import Background

logger = get_logger()


@dataclass
class Audio:
    """Audio class: Represent audio data to be played in a node."""

    music: str | None = None
    atmosphere: str | None = None
    sound: str | None = None


class Node(GameEntity, ABC):
    """Node class: Represent a node of the game story."""

    _mandatory_attributes: ClassVar[list[str]]

    def __init__(
        self,
        uuid: str,
        next_uuid: str,
        background: Background | None = None,
        audio: Audio | None = None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.next_uuid = next_uuid
        self.audio = audio
        self.background = background
        self.done = False

    @classmethod
    def check_attributes(cls, attributes: dict[str, Any]) -> None:
        if all(attr in attributes for attr in cls._mandatory_attributes):
            return

        raise ValueError(f"Missing mandatory attributes for {cls.__name__} node.")

    def setup(self) -> None:
        """Setup node. Audio is managed here."""
        if self.audio is None:
            return

        if self.audio.music is not None:
            mixer.play_music(self.audio.music)
        elif self.audio.atmosphere is not None:
            mixer.play_atmos(self.audio.atmosphere)
        elif self.audio.sound is not None:
            # TODO: Play sound effect
            pass

    def process_event(self, event: Event) -> None:
        pass

    def teardown(self) -> None:
        pass


class NullNode(Node):
    """Null node class: Represent a null node of the game story."""

    def __init__(self) -> None:
        super().__init__(uuid="null", next_uuid="null")

    def setup(self) -> None:
        pass

    def process_event(self, event: Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        pass

    def teardown(self) -> None:
        pass
