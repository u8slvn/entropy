from __future__ import annotations

from enum import IntEnum

import pygame

import entropy


class Channel(IntEnum):
    GENERAL = 0
    MUSIC = 1
    ATMOSPHERE = 2
    VOICE = 3
    UISFX = 4


class Mixer:
    def __init__(
        self,
        general_vol: float = 1.0,
        music_vol: float = 1.0,
        atmos_vol: float = 1.0,
        voice_vol: float = 1.0,
        ui_sfx_vol: float = 1.0,
    ):
        pygame.mixer.init(frequency=48000, buffer=2048)
        self._volumes = {
            Channel.GENERAL: general_vol,
            Channel.MUSIC: music_vol,
            Channel.ATMOSPHERE: atmos_vol,
            Channel.VOICE: voice_vol,
            Channel.UISFX: ui_sfx_vol,
        }
        self._channels = {
            Channel.MUSIC: pygame.mixer.Channel(Channel.MUSIC),
            Channel.ATMOSPHERE: pygame.mixer.Channel(Channel.ATMOSPHERE),
            Channel.VOICE: pygame.mixer.Channel(Channel.VOICE),
            Channel.UISFX: pygame.mixer.Channel(Channel.UISFX),
        }
        self._refresh_volume()

    def play_music(self, name: str) -> None:
        sound = entropy.assets.sound.get(name=name)
        self._channels[Channel.MUSIC].play(sound, -1)

    def play_atmos(self, sound: pygame.mixer.Sound) -> None:
        self._channels[Channel.ATMOSPHERE].play(sound, -1)

    def play_voice(self, sound: pygame.mixer.Sound) -> None:
        self._channels[Channel.ATMOSPHERE].play(sound)

    def play_uisfx(self, name: str) -> None:
        sound = entropy.assets.sound.get(name=name)
        self._channels[Channel.UISFX].queue(sound)

    def set_volume(self, value: float, channel: Channel):
        assert 0.0 <= value <= 1.0
        self._volumes[channel] = value

        if channel == Channel.GENERAL:
            self._refresh_volume()
        else:
            self._refresh_volume(channel=channel)

    def _refresh_volume(self, channel: Channel | None = None) -> None:
        channels = [channel] if channel is not None else self._channels.keys()

        for channel in channels:
            volume = self._volumes[Channel.GENERAL] * self._volumes[channel]
            self._channels[channel].set_volume(volume)
