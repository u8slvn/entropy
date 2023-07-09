from __future__ import annotations

from collections import OrderedDict

import pygame

from entropy import Monitor


class Resolution:
    def __init__(self, alias: str, width: int, height: int) -> None:
        self.alias = alias
        self.width = width
        self.height = height
        self.flags = pygame.SCALED

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def display_name(self) -> str:
        return f"{self.width}x{self.height}"


class FullScreenResolution(Resolution):
    def __init__(self, alias: str, width: int, height: int) -> None:
        super().__init__(alias=alias, width=width, height=height)
        self.flags += pygame.FULLSCREEN

    @property
    def display_name(self):
        return self.alias


class Resolutions:
    def __init__(self) -> None:
        self._resolutions: dict[str, Resolution] = OrderedDict()

    def add(self, resolution: Resolution) -> None:
        self._resolutions[resolution.alias] = resolution

    def get(self, alias: str) -> Resolution:
        return self._resolutions[alias]

    @classmethod
    def build_resolutions(
        cls, static_res: list[tuple[str, int, int]], monitor: Monitor
    ) -> Resolutions:
        resolutions = cls()
        for res in static_res:
            resolutions.add(Resolution(*res))
        resolutions.add(FullScreenResolution("FULLSCREEN", *monitor.size))

        return resolutions
