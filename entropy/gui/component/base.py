from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Generic
from typing import TypeVar

import pygame as pg


if TYPE_CHECKING:
    from entropy.event.event import Event


class Sprite(pg.sprite.DirtySprite):
    def process_event(self, event: Event) -> None:
        pass

    def move(self, **kwargs: Any) -> None:
        if self.image is not None:
            self.rect = self.image.get_rect(**kwargs)

    def teardown(self) -> None:
        pass


_Sprite = TypeVar("_Sprite", bound=Sprite)


class SpriteGroup(pg.sprite.LayeredUpdates, Generic[_Sprite]):
    def process_event(self, event: Event) -> None:
        for sprite in self.sprites():
            sprite.process_event(event)

    def teardown(self) -> None:
        for sprite in self.sprites():
            sprite.teardown()
