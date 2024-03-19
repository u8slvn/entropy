from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any


if TYPE_CHECKING:
    from entropy.game.story.nodes.base import Node


class NodeBuilder:

    @classmethod
    def build(cls, data: dict[str, Any]) -> Node:
        """Build a node from the given data."""
        template = data.pop("template")
        # background = data.pop("background")
        # audio = Audio(**data.pop("audio", {}))
        return getattr(cls, f"_build_{template}")(data)

    def _build_contemplation(self, data: dict[str, Any]) -> Node:
        pass

    def _build_dialog(self, data: dict[str, Any]) -> Node:
        pass

    def _build_event(self, data: dict[str, Any]) -> Node:
        pass

    def _build_intro(self, data: dict[str, Any]) -> Node:
        pass

    def _build_outro(self, data: dict[str, Any]) -> Node:
        pass

    def _build_transition(self, data: dict[str, Any]) -> Node:
        pass
