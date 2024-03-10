from __future__ import annotations

import pygame as pg


class GUIComponent(pg.sprite.Sprite):
    pass


class GUIGroup(pg.sprite.LayeredUpdates[GUIComponent]):
    pass
