from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import ClassVar
from typing import Generic
from typing import TypeVar


T = TypeVar("T")


class AssetsCollection(ABC):
    """Base class for an asset's collection."""

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def load(self, name: str | None = None) -> None:
        """Load the asset with the given name."""
        ...

    @abstractmethod
    def debug(self) -> None:
        """Print the debug information of the collection."""
        ...


class DirAssetsCollection(AssetsCollection, ABC, Generic[T]):
    """Base class for an asset's collection based on a directory. The extensions class
    variable is used to filter the files in the directory.
    """

    extensions: ClassVar[list[str]]

    def __init__(self, name: str):
        super().__init__(name=name)
        self._cache: dict[str, T] = {}
        self._files: dict[str, Path] = {}

    def add_dir(self, path: str | Path) -> None:
        """Add a directory to the collection."""
        path = Path(path) if isinstance(path, str) else path
        for item in path.iterdir():
            if item.is_dir():
                self.add_dir(path=item)
            elif item.suffix in self.extensions:
                self._files[item.stem] = item

    @abstractmethod
    def _load_file(self, file: Path) -> T:
        """Load the asset from the given filepath."""
        ...

    def load(self, name: str | None = None) -> None:
        """Load the asset with the given name."""
        names = [name] if name else self._files.keys()
        for name in names:
            self._cache[name] = self._load_file(self._files[name])

    def get(self, name: str) -> T:
        """Return the asset with the given name."""
        if self._cache.get(name) is None:
            self.load(name)

        return self._cache[name]

    def clear_cache(self) -> None:
        """Clear the cache of the collection."""
        self._cache.clear()
