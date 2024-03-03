from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from entropy import mixer
from entropy.game.entity import GameEntity
from entropy.logging import get_logger


if TYPE_CHECKING:
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
    ):
        super().__init__()
        self.chapter = chapter
        self.next_id = next_id

        if music is not None:
            mixer.play_music(music)

        if background is not None:
            self.chapter.set_background(config=background)

    def mark_as_done(self) -> None:
        super().mark_as_done()
        self.transition_to_next()

    def transition_to_next(self):
        self.chapter.transition_to_node(id_=self.next_id)
