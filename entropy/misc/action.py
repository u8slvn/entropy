from __future__ import annotations

import pygame as pg


class Actions:
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.ENTER = False
        self.SPACE = False
        self.F5 = False
        self.F6 = False

    def parse_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.UP = True
            elif event.key == pg.K_DOWN:
                self.DOWN = True
            elif event.key == pg.K_RETURN:
                self.ENTER = True
            elif event.key == pg.K_SPACE:
                self.SPACE = True
            elif event.key == pg.K_F5:
                self.F5 = True
            elif event.key == pg.K_F6:
                self.F6 = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.UP = False
            elif event.key == pg.K_DOWN:
                self.DOWN = False
            elif event.key == pg.K_RETURN:
                self.ENTER = False
            elif event.key == pg.K_SPACE:
                self.SPACE = False
            elif event.key == pg.K_F5:
                self.F5 = False
            elif event.key == pg.K_F6:
                self.F6 = False

    def reset(self) -> None:
        for action in self.__dict__.keys():
            setattr(self, action, False)
