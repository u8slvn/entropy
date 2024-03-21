from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import cast

from entropy.game.story.nodes.base import Audio
from entropy.game.story.nodes.intro import IntroNode


if TYPE_CHECKING:
    from entropy.game.story.nodes.base import Node
    from entropy.gui.elements.background import Background


class NodeBuilder:
    """NodeBuilder class: Build a node from the given data."""

    @classmethod
    def build(cls, data: dict[str, Any]) -> Node:
        """Build a node from the given data."""
        template = data.pop("template")
        background = data.pop("background")
        audio = Audio(**data.pop("audio", {}))

        try:
            return cast(
                Node, getattr(cls, f"_build_{template}")(background, audio, data)
            )
        except AttributeError:
            raise ValueError(f"Unknown node template: {template}.")

    @classmethod
    def _build_intro(
        cls, background: Background, audio: Audio, data: dict[str, Any]
    ) -> Node:
        """Build an intro node."""
        elements = data.pop("elements")
        title = ElementBuilder.build(elements["title"])
        subtitle = ElementBuilder.build(**elements.pop("subtitle"))

        return IntroNode(
            uuid=data["uuid"],
            next_uuid=data["next_uuid"],
            background=background,
            audio=audio,
            attributes={
                "title": title,
                "subtitle": subtitle,
                # "ease_in": attributes["ease-in"],
                # "ease_out": attributes["ease-out"],
            },
        )


class ElementBuilder:
    @classmethod
    def build(cls, template, **kwargs) -> Any:

        try:
            return getattr(cls, f"_build_{template}")(**kwargs)
        except AttributeError:
            raise ValueError(f"Unknown element template: {template}.")
