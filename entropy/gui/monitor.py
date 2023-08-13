from __future__ import annotations

import pygame

from entropy.logging import get_logger
from entropy.utils import Res


logger = get_logger()


class Monitor:
    def __init__(self) -> None:
        self.info = pygame.display.Info()
        logger.info(f'Monitor native resolution is "{self.res}".')

    @property
    def res(self) -> Res:
        return Res(self.info.current_w, self.info.current_h)
