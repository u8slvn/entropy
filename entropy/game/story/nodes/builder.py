from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any


if TYPE_CHECKING:
    from entropy.game.story.nodes.base import Node


class NodeBuilder:

    @classmethod
    def build(cls, node_data: dict[str, Any]) -> Node:
        """Build a node from the given data."""
        node_type = node_data.pop("type")
        return getattr(cls, f"_build_{node_type}")(node_data)

    def _build_contemplation(self, node_data: dict[str, Any]) -> Node:
        pass

    def _build_dialog(self, node_data: dict[str, Any]) -> Node:
        pass

    def _build_event(self, node_data: dict[str, Any]) -> Node:
        pass

    def _build_intro(self, node_data: dict[str, Any]) -> Node:
        pass

    def _build_outro(self, node_data: dict[str, Any]) -> Node:
        pass

    def _build_transition(self, node_data: dict[str, Any]) -> Node:
        pass
