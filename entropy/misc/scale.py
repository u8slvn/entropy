from __future__ import annotations

import functools
from typing import TYPE_CHECKING

import pygame

from entropy.misc.assets import Image
from entropy.misc.rect import Rect


if TYPE_CHECKING:
    from entropy import Game


class Scaler:
    def __init__(self, game: Game):
        self.game = game

    @functools.singledispatchmethod
    def scale(self, _item) -> None:
        raise NotImplementedError(f"Cannot scale {_item}")

    @scale.register(Image)
    def _(self, _item: Image) -> None:
        if self.game.at_max_resolution():
            _item.surface = _item.original
        else:
            w = round(_item.scale_percent_w * self.game.screen_resolution.width)
            h = round(_item.scale_percent_h * self.game.screen_resolution.height)
            _item.surface = pygame.transform.scale(_item.original, (w, h))

    @scale.register(Rect)
    def _(self, _item: Rect) -> None:
        _item.rect = pygame.Rect(_item.original)

        if not self.game.at_max_resolution():
            _item.rect.x = round(
                _item.scale_percent_x * self.game.screen_resolution.width
            )
            _item.rect.w = round(
                _item.scale_percent_w * self.game.screen_resolution.width
            )
            _item.rect.y = round(
                _item.scale_percent_y * self.game.screen_resolution.height
            )
            _item.rect.h = round(
                _item.scale_percent_h * self.game.screen_resolution.height
            )
