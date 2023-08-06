from __future__ import annotations

from entropy import config
from entropy import window
from entropy.commands.base import Command


class EnableFullscreen(Command):
    def __call__(self) -> None:
        if window.fullscreen is True:
            return

        window.toggle_fullscreen()
        config.update_attr(name="fullscreen", value=True)


class DisableFullscreen(Command):
    def __call__(self) -> None:
        if window.fullscreen is False:
            return

        window.toggle_fullscreen()
        config.update_attr(name="fullscreen", value=False)
