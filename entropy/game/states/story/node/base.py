from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from entropy import mixer
from entropy.game.entity import GameEntity
from entropy.game.states.story.factory import build_transition
from entropy.logging import get_logger


if TYPE_CHECKING:
    import pygame

    from entropy.game.states.story import Chapter

logger = get_logger()


class BaseNode(GameEntity, ABC):
    def __init__(self):
        self._done = False

    def mark_as_done(self) -> None:
        self._done = True

    def is_done(self) -> bool:
        return self._done

    def setup(self) -> None:
        self._done = False

    def teardown(self) -> None:
        self._done = False


class Node(BaseNode, ABC):
    def __init__(
        self,
        chapter: Chapter,
        next_id: str,
        music: str | None = None,
        background: str | None = None,
        ease_in: dict[str, str | int] | None = None,
        ease_out: dict[str, str | int] | None = None,
    ):
        super().__init__()
        self.chapter = chapter
        self.next_id = next_id
        self._ready = False
        self._ease_in = None
        self._ease_out = None

        if music is not None:
            mixer.play_music(music)
        if background is not None:
            self.chapter.set_background(config=background)
        if ease_in is not None:
            self._ease_in = build_transition(
                params=ease_in, callback=self.mark_as_ready
            )
        if ease_out is not None:
            self._ease_out = build_transition(
                params=ease_out, callback=self.mark_as_done
            )

    def mark_as_ready(self) -> None:
        self._ready = True

    def is_ready(self) -> bool:
        return self._ready

    def close(self):
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
