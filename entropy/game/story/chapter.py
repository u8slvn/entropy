from __future__ import annotations

import json

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from entropy.game.story.nodes.base import Node
from entropy.game.story.nodes.base import NullNode
from entropy.game.story.nodes.builder import NodeBuilder


@dataclass
class ChapterCollection:
    """ChapterCollection class: Represent a collection of chapters."""

    file_extension = ".entropy"

    def __init__(self, dir_path: Path, index_file: str) -> None:
        self._dir_path = dir_path
        self._index_file = index_file
        self._chapters_index: dict[str, Any] = self._load_index()

    def _load_index(self) -> Any:
        """Load the index file. It contains the chapters and their entrypoints."""
        index_path = self._dir_path / f"{self._index_file}{self.file_extension}"
        with open(index_path, "r") as file:
            return json.load(file)

    def load_chapter(self, name: str) -> Chapter:
        """Load and build the chapter with the given name."""
        try:
            entrypoint = self._chapters_index[name]
        except KeyError:
            raise ValueError(f'Chapter with name "{name}" does not exist.')

        chapter_path = self._dir_path / f"{name}{self.file_extension}"
        with open(chapter_path, "r") as file:
            nodes_data = json.load(file)

        nodes: dict[str, Node] = {}
        for uuid, data in nodes_data.items():
            nodes[uuid] = NodeBuilder.build(data)

        return Chapter(entrypoint, nodes)


@dataclass
class Chapter:
    """Chapter class: Represent a chapter of the game. Each chapter contains an
    entrypoint and a collection of nodes. The entrypoint is the first node uuid.
    """

    entrypoint: str
    nodes: dict[str, Node]

    def get_node(self, uuid: str | None = None) -> Node:
        """Return the node with the given uuid."""
        uuid = uuid or self.entrypoint
        try:
            return self.nodes[uuid]
        except KeyError:
            raise ValueError(f'Node with uuid "{uuid}" does not exist.')


class NullChapter(Chapter):
    """NullChapter class: Represent a null chapter of the game."""

    def __init__(self) -> None:
        super().__init__("", {})

    def get_node(self, uuid: str | None = None) -> Node:
        """Implement the get_node method for the NullChapter which obviously returns a
        NullNode.
        """
        return NullNode()
