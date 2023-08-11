from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path
from typing import Any

from entropy.logger import get_logger
from entropy.tools.observer import Subject
from entropy.utils import Res


logger = get_logger()


class Config(Subject):
    _default_config = OrderedDict(
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
                    "font": "",
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
