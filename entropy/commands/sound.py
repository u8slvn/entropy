from __future__ import annotations

from entropy import mixer
from entropy.commands.base import ConfigurableCommand
from entropy.mixer import Channel


class SetVolume(ConfigurableCommand):
    def __init__(self, channel: Channel) -> None:
        super().__init__()
        self._channel = channel

    def __call__(self) -> None:
        mixer.set_volume(*self._args, channel=self._channel)
