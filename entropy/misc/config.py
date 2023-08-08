from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path
from typing import Any

from entropy import get_logger
from entropy.tools.observer import Observer
from entropy.utils import Res


logger = get_logger()


class Config(Observer):
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
                    "font": "",
                    "locale": "en",
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

        logger.info("Config loaded.")

    @property
    def res(self) -> Res:
        return Res(self.resolution_x, self.resolution_y)

    @res.setter
    def res(self, res: Res) -> None:
        self.resolution_x, self.resolution_y = res
        self.save()

    def notify(self) -> None:
        for subject in self._registered_subjects:
            subject.update()

    def update_attr(self, name: str, value: Any):
        setattr(self, name, value)
        self.notify()
        self.save()

    def save(self):
        # Display
        self._config["display"]["fps"] = str(self.fps)
        self._config["display"]["resolution_x"] = str(self.resolution_x)
        self._config["display"]["resolution_y"] = str(self.resolution_y)
        self._config["display"]["fullscreen"] = str(self.fullscreen)

        # Game
        self._config["game"]["locale"] = str(self.locale)

        try:
            if not self._config_file.exists():
                self._config_file.touch(mode=0o600)

            with self._config_file.open("w") as file:
                self._config.write(file)
        except OSError as error:
            logger.error(f"Cannot save config file: {error}")

    @classmethod
    def get_default_config(cls) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read_dict(cls._default_config)
        return config
