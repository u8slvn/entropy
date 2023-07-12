from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import pygame.font

from entropy.misc.resolution import Resolution


if TYPE_CHECKING:
    from entropy.misc.game import Game


class Asset:
    def __init__(self, name: str) -> None:
        self.name = name


class Font(Asset):
    split_char = "_"

    def __init__(
        self,
        name: str,
        fonts: dict[str, pygame.font.Font],
        scale_percents: dict[str, float],
    ) -> None:
        super().__init__(name=name)
        self.originals = fonts
        self.fonts = self.originals.copy()
        self.scale_percents = scale_percents

    @classmethod
    def from_file(
        cls, file: Path, sizes: dict[str, int], resolution: Resolution
    ) -> Font:
        name = file.stem
        fonts = {
            alias.upper(): pygame.font.Font(file, size) for alias, size in sizes.items()
        }
        scale_percents = {
            alias: size / resolution.height for alias, size in sizes.items()
        }

        return cls(name=name, fonts=fonts, scale_percents=scale_percents)

    def size(self, size: str) -> pygame.font.Font:
        return self.fonts[size]


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


TAsset = TypeVar("TAsset", bound="Asset")


class AssetsCollection(ABC):
    asset_type: TAsset

    def __init__(self) -> None:
        self.assets: dict[str, TAsset] = {}

    @abstractmethod
    def load(self, resolution: Resolution) -> None:
        ...


class DirAssetsCollection(AssetsCollection):
    extensions: list[str]

    def __init__(self) -> None:
        super().__init__()
        self._files: list[Path] = []

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files.append(item)

    def load(self, resolution: Resolution) -> None:
        for file in self._files:
            asset = self.asset_type.from_file(
                file=file,
                resolution=resolution,
            )
            self.assets[asset.name] = asset

    def get(self, name: str) -> Asset:
        return self.assets[name]


class ImagesCollection(DirAssetsCollection):
    asset_type = Image
    extensions = [".png"]


class FontsCollection(AssetsCollection):
    asset_type = Font

    def __init__(self) -> None:
        super().__init__()
        self._font_configs: list[tuple[Path, dict[str, int]]] = []

    def add_font(self, path: str | Path, **sizes: int):
        path = Path(path) if isinstance(path, str) else path
        self._font_configs.append((path, sizes))

    def get(self, name: str, size: str) -> Font:
        return self.assets[name].size(size)

    def load(self, resolution: Resolution) -> None:
        for config in self._font_configs:
            file, sizes = config
            asset = Font.from_file(file=file, sizes=sizes, resolution=resolution)
            self.assets[asset.name] = asset


class AssetsLibrary:
    def __init__(self) -> None:
        self.game: Game | None = None
        self.fonts = FontsCollection()
        self.images = ImagesCollection()

    def setup(self, game: Game):
        self.game = game
        self.fonts.load(resolution=self.game.max_resolution)
        self.images.load(resolution=self.game.max_resolution)
        self.scale()

    def scale(self) -> None:
        for _, image in self.images.assets.items():
            self.game.scaler.scale(image)
