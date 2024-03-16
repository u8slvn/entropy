from __future__ import annotations

import json

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Generator

from entropy.locations import STORY_DIR


if TYPE_CHECKING:
    from entropy.game.story.nodes.base import Node


class Chapters:
    """Chapters class: Represent a collection of chapters of the game."""

    _dir_path = STORY_DIR
    _index_file = "index"
    _ext_file = ".entropy"

    def __init__(self):
        self._index = self._load_index()

    def _load_index(self) -> dict[str, str]:
        """
        Load the index file of the chapters which determine the filename and the
        entrypoint of each chapter.
        """
        with open(self._dir_path / f"{self._index_file}{self._ext_file}", "r") as file:
            return json.load(file)

    def _load_chapter(self, filename, entrypoint) -> Chapter:
        """Load the chapter from the given filename."""
        with open(self._dir_path / f"{filename}{self._ext_file}", "r") as file:
            nodes = json.load(file)

        return Chapter(entrypoint, nodes)

    def get_chapter(self) -> Generator[Chapter, None, None]:
        """Generator to get all the chapters."""
        for chapter, entrypoint in self._index.items():
            yield self._load_chapter(chapter, entrypoint)


@dataclass
class Chapter:
    entrypoint: str
    nodes: list[dict[str:Any]]

    def get_node(self, uuid: str) -> Node | None:
        """Return the node with the given uuid."""
        for node in self.nodes:
            if node["uuid"] == uuid:
                return node
        return None
