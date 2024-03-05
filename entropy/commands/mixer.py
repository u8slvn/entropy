from __future__ import annotations

from entropy import mixer
from entropy.commands.base import Command


class PlayVoice(Command):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def __call__(self) -> None:
        if not mixer.voice_is_busy():
            mixer.play_voice(name=self._name)


class SaveMixerVolume(Command):
    def __call__(self) -> None:
        mixer.save_volumes()
