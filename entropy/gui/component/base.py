from __future__ import annotations

import pygame as pg


class Sprite(pg.sprite.DirtySprite):
    pass


class SpriteGroup(pg.sprite.LayeredUpdates):
    pass
