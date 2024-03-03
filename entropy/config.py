from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path
from typing import Any
from typing import ClassVar

from entropy.locations import CONFIG_FILE_PATH
from entropy.logging import get_logger
from entropy.tools.observer import Subject
from entropy.utils import Res


logger = get_logger()

_config: _Config | None = None


def get_config() -> _Config:
    global _config

    if _config is None:
        _config = _Config(config_file=CONFIG_FILE_PATH)

    return _config


class _Config(Subject):
    _default_config: ClassVar[OrderedDict] = OrderedDict(
        {
            "display": OrderedDict(
                {
                    "fps": 60,
                    "resolution_x": 1600,
                    "resolution_y": 900,
                    "fullscreen": False,
                }
            ),
            "game": OrderedDict(
                {
                    "locale": "en",
                    "font": "LanaPixel",
                    "text_speed": 2,
                }
            ),
            "sound": OrderedDict(
                {
                    "main_volume": 1.0,
                    "music_volume": 1.0,
                    "atmosphere_volume": 1.0,
                    "voice_volume": 1.0,
                    "uisfx_volume": 1.0,
                }
            ),
        }
    )

    def __init__(self, config_file: Path | None = None) -> None:
        super().__init__()
        self._config_file = config_file
        self._config = self.get_default_config()

        if self._config_file is not None:
            self._config.read(self._config_file)

        # Display
        self.fps = self._config.getfloat("display", "fps")
        self.resolution_x = self._config.getint("display", "resolution_x")
        self.resolution_y = self._config.getint("display", "resolution_y")
        self.fullscreen = self._config.getboolean("display", "fullscreen")

        # Game
        self.locale = self._config.get("game", "locale")
        self.font = self._config.get("game", "font")
        self.text_speed = self._config.getfloat("game", "text_speed")

        # Sound
        self.main_volume = self._config.getfloat("sound", "main_volume")
        self.music_volume = self._config.getfloat("sound", "music_volume")
        self.atmosphere_volume = self._config.getfloat("sound", "atmosphere_volume")
        self.voice_volume = self._config.getfloat("sound", "voice_volume")
        self.uisfx_volume = self._config.getfloat("sound", "uisfx_volume")

        logger.info("Config loaded.")

    @property
    def res(self) -> Res:
        return Res(self.resolution_x, self.resolution_y)

    @res.setter
    def res(self, res: Res) -> None:
        self.resolution_x, self.resolution_y = res
        self.notify()

    def update_attr(self, name: str, value: Any):
        setattr(self, name, value)
        self.notify()

    def save(self):
        for section, params in self._default_config.items():
            for param in params.keys():
                self._config[section][param] = str(getattr(self, param))

        try:
            if not self._config_file.exists():
                self._config_file.touch(mode=0o600)

            with self._config_file.open("w") as file:
                self._config.write(file)
        except OSError as error:
            logger.error(f"Cannot save config file: {error}")

        logger.info("Config saved.")

    @classmethod
    def get_default_config(cls) -> configparser.ConfigParser:
        config = configparser.ConfigParser(dict_type=OrderedDict)
        config.read_dict(cls._default_config)
        return config
