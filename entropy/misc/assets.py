from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING, Any, Type

import pygame.font

from entropy.misc.resolution import Resolution


if TYPE_CHECKING:
    from entropy.misc.game import Game


class Asset(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    @abstractmethod
    def from_file(cls, file: Path, resolution: Resolution) -> Asset | list[Asset]:
        ...


class Font(Asset):
    split_char = "_"

    def __init__(
        self,
        name: str,
        fonts: dict[int, pygame.font.Font],
        scale_percents: dict[int, float],
    ) -> None:
        super().__init__(name=name)
        self.originals = fonts
        self.fonts = self.originals.copy()
        self.scale_percents = scale_percents

    @classmethod
    def from_file(cls, file: Path, resolution: Resolution) -> Font:
        name, sizes = file.stem.split(cls.split_char)
        sizes = sizes.split("-")
        fonts = {int(size): pygame.font.Font(file, int(size)) for size in sizes}
        scale_percents = {size: size / resolution.height for size in fonts.keys()}

        return cls(name=name, fonts=fonts, scale_percents=scale_percents)

    def size(self, _size: int) -> pygame.font.Font:
        return self.fonts[_size]


class Image(Asset):
    alpha_suffix = "-a"

    def __init__(
        self, name: str, image: pygame.Surface, scale_percent: tuple[float, float]
    ) -> None:
        super().__init__(name=name)
        self.original = image
        self.surface = self.original
        self.scale_percent = scale_percent

    @property
    def scale_percent_w(self):
        return self.scale_percent[0]

    @property
    def scale_percent_h(self):
        return self.scale_percent[1]

    @classmethod
    def from_file(cls, file: Path, resolution: Resolution) -> Image:
        name = file.stem
        if name.endswith(cls.alpha_suffix):
            image = pygame.image.load(file).convert_alpha()
        else:
            image = pygame.image.load(file).convert()

        scale_percent = (
            image.get_width() / resolution.width,
            image.get_height() / resolution.height,
        )

        return cls(name=name, image=image, scale_percent=scale_percent)


class AssetsManager(ABC):
    asset_type: Type[Asset]
    extensions: list[str]

    def __init__(self) -> None:
        self._files: deque[Path] = deque()
        self.assets: dict[str, Any] = {}

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files.append(item)

    @property
    def nb_files(self) -> int:
        return len(self._files)

    def load(self, resolution: Resolution) -> None:
        for file in self._files:
            asset = self.asset_type.from_file(
                file=file,
                resolution=resolution,
            )
            self.assets[asset.name] = asset


class FontsManager(AssetsManager):
    asset_type = Font
    extensions = [".ttf"]

    def get(self, name: str, size: int) -> Font:
        return self.assets[name].size(size)


class ImagesManager(AssetsManager):
    asset_type = Image
    extensions = [".png"]

    def get(self, name: str) -> Image:
        return self.assets[name]


class Assets:
    def __init__(self, game: Game):
        self.game = game
        self.fonts = FontsManager()
        self.images = ImagesManager()

    def load(self) -> None:
        self.fonts.load(resolution=self.game.max_resolution)
        self.images.load(resolution=self.game.max_resolution)
        self.scale()

    def scale(self) -> None:
        for _, image in self.images.assets.items():
            self.game.scaler.scale(image=image)
