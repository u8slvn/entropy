from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any


class AssetsCollection(ABC):
    @abstractmethod
    def load(self) -> None: ...


class DirAssetsCollection(AssetsCollection, ABC):
    extensions: list[str]

    def __init__(self) -> None:
        self.assets: dict[str, Any] = {}
        self._files: list[Path] = []

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files.append(item)

    @abstractmethod
    def _load_file(self, file: Path) -> Any: ...

    def load(self) -> None:
        for file in self._files:
            self.assets[file.stem] = self._load_file(file=file)

    def get(self, name: str) -> Any:
        return self.assets[name]
