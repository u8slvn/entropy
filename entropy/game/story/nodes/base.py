from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from typing import Any

from entropy import mixer
from entropy.event.event import Event
from entropy.game.entity import GameEntity
from entropy.game.states.story.factory import build_transition
from entropy.logging import get_logger


if TYPE_CHECKING:
    import pygame


logger = get_logger()


class BaseNode(GameEntity, ABC):
    """Base class for a Node."""

    def __init__(self) -> None:
        self._done = False

    def mark_as_done(self) -> None:
        """Mark the node as done."""
        self._done = True

    def is_done(self) -> bool:
        """Return True if the node is done."""
        return self._done


class Node(BaseNode, ABC):
    """Node class: Represent a node of the game story."""

    def __init__(
        self,
        next_id: str,
        music: str | None = None,
        background: str | None = None,
        ease_in: dict[str, Any] | None = None,
        ease_out: dict[str, Any] | None = None,
    ):
        super().__init__()
        self.next_id = next_id
        self.background = background
        self._ready = False
        self._ease_in = None
        self._ease_out = None

        if music is not None:
            mixer.play_music(music)
        if ease_in is not None:
            self._ease_in = build_transition(
                params=ease_in, callback=self.mark_as_ready
            )
        if ease_out is not None:
            self._ease_out = build_transition(
                params=ease_out, callback=self.mark_as_done
            )

    def mark_as_ready(self) -> None:
        """Mark the node as ready. It means that the ease_in transition is done."""
        self._ready = True

    def is_ready(self) -> bool:
        """Check if the node is ready."""
        return self._ready

    def close(self) -> None:
        if self._ease_out is not None:
            self._ease_out.activate()
        else:
            self.mark_as_done()

    def setup(self) -> None:
        if self._ease_in is not None:
            self._ease_in.setup()
        if self._ease_out is not None:
            self._ease_out.setup()

    def update(self, dt: float) -> None:
        if self._ease_in is not None:
            self._ease_in.update(dt=dt)
        if self._ease_out is not None:
            self._ease_out.update(dt=dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self._ease_in is not None:
            self._ease_in.draw(surface=surface)
        if self._ease_out is not None:
            self._ease_out.draw(surface=surface)

    def teardown(self) -> None:
        if self._ease_in:
            self._ease_in.teardown()
        if self._ease_out is not None:
            self._ease_out.teardown()


class NullNode(Node):
    """Null Node: A node that does nothing."""

    def __init__(self) -> None:
        super().__init__(next_id="end")

    def process_event(self, event: Event) -> None:
        pass
