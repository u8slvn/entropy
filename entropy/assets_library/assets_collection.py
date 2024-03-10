from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import ClassVar
from typing import Generic
from typing import TypeVar


T = TypeVar("T")


class AssetsCollection(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def load(self, name: str | None = None) -> None: ...

    @abstractmethod
    def debug(self) -> None: ...


class DirAssetsCollection(AssetsCollection, ABC, Generic[T]):
    extensions: ClassVar[list[str]]

    def __init__(self, name: str):
        super().__init__(name=name)
        self._cache: dict[str, T] = {}
        self._files: dict[str, Path] = {}

    def add_dir(self, path: str | Path) -> None:
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files[item.stem] = item

    @abstractmethod
    def _load_file(self, file: Path) -> T: ...

    def load(self, name: str | None = None) -> None:
        names = [name] if name else self._files.keys()
        for name in names:
            self._cache[name] = self._load_file(self._files[name])

    def get(self, name: str) -> T:
        if self._cache.get(name) is None:
            self.load(name)

        return self._cache[name]

    def clear_cache(self) -> None:
        self._cache.clear()
