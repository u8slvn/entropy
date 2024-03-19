from __future__ import annotations

import json

from dataclasses import dataclass
from typing import Any

from entropy.game.story.nodes.base import Node
from entropy.game.story.nodes.base import NullNode
from entropy.locations import STORY_DIR


class Chapters:
    """Chapters class: Represent a collection of chapters of the game."""

    _dir_path = STORY_DIR
    _index_file = "index"
    _ext_file = ".entropy"

    def __init__(self, chapters: dict[str, Chapter]) -> None:
        self._chapters = chapters

    @classmethod
    def _load_index(cls) -> Any:
        """Load the index file of the chapters which determine the filename and the
        entrypoint of each chapter.
        """
        with open(cls._dir_path / f"{cls._index_file}{cls._ext_file}", "r") as file:
            return json.load(file)

    @classmethod
    def load_chapters(cls) -> Chapters:
        """Load the chapters from index file and the nodes files of each chapter."""
        chapters = {}
        index = cls._load_index()
        for chapter, data in index.items():
            with open(cls._dir_path / f"{chapter}{cls._ext_file}", "r") as file:
                nodes = json.load(file)

            chapters[chapter] = Chapter(data["entrypoint"], nodes)

        return cls(chapters)

    def get_chapter(self, name: str) -> Chapter:
        """Return the chapter with the given name."""
        try:
            return self._chapters[name]
        except KeyError:
            raise ValueError(f'Chapter with name "{name}" does not exist.')


@dataclass
class Chapter:
    """Chapter class: Represent a chapter of the game. Each chapter contains an entrypoint
    and a collection of nodes. The entrypoint is the first node uuid.
    """

    entrypoint: str
    nodes: dict[str, dict[str, Any]]

    def get_node(self, uuid: str | None = None) -> Node:
        """Return the node with the given uuid."""
        uuid = uuid or self.entrypoint
        if node := self.nodes.get(uuid):
            return Node(**node)

        return NullNode()


class NullChapter(Chapter):
    """NullChapter class: Represent a null chapter of the game."""

    def __init__(self) -> None:
        super().__init__("", {})

    def get_node(self, uuid: str | None = None) -> Node:
        return NullNode()
