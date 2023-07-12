from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakSet

import pygame

from entropy.misc.resolution import Resolution


if TYPE_CHECKING:
    from entropy.misc.assets import Image
    from entropy.misc.scale import Scaler


class Rect:
    def __init__(
        self, rect: pygame.Rect, scale_percent: tuple[float, float, float, float]
    ) -> None:
        global rect_collection

        self.original = rect
        self.rect = self.original
        self.scale_percent = scale_percent

        rect_collection.add(self)

    @property
    def scale_percent_x(self):
        return self.scale_percent[0]

    @property
    def scale_percent_y(self):
        return self.scale_percent[1]

    @property
    def scale_percent_w(self):
        return self.scale_percent[2]

    @property
    def scale_percent_h(self):
        return self.scale_percent[3]

    @classmethod
    def from_image(cls, x: int, y: int, image: Image) -> Rect:
        global rect_collection

        rect = image.original.get_rect()
        rect.topleft = (x, y)
        scale_x = x / rect_collection.max_resolution.width
        scale_y = y / rect_collection.max_resolution.height
        scale_w = rect.width / rect_collection.max_resolution.width
        scale_h = rect.height / rect_collection.max_resolution.height
        scale_percent = (scale_x, scale_y, scale_w, scale_h)

        return cls(rect=rect, scale_percent=scale_percent)


class _RectCollection:
    def __init__(self):
        self._rect_collection: WeakSet[Rect] = WeakSet()
        self._scaler: Scaler | None = None
        self.max_resolution: Resolution | None = None

    def setup(self, scaler: Scaler):
        self._scaler = scaler
        self.max_resolution = scaler.game.max_resolution

    def add(self, rect: Rect) -> None:
        self._rect_collection.add(item=rect)

    def scale(self):
        for rect in self._rect_collection:
            self._scaler.scale(rect)


rect_collection = _RectCollection()
