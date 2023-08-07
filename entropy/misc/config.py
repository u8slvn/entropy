from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path
from typing import Any

from entropy.tools.observer import Observer
from entropy.utils import Res


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
            "locale": OrderedDict(
                {
                    "lang": "en",
                }
            ),
        }
    )

    def __init__(self, config_file: Path | None = None) -> None:
        super().__init__()
        config = self.get_default_config()

        if config_file is not None:
            config.read(config_file)

        self.fps = config.getfloat("display", "fps")
        self.resolution_x = config.getint("display", "resolution_x")
        self.resolution_y = config.getint("display", "resolution_y")
        self.fullscreen = config.getboolean("display", "fullscreen")
        self.lang = config.get("locale", "lang")

    @property
    def res(self) -> Res:
        return Res(self.resolution_x, self.resolution_y)

    @res.setter
    def res(self, res: Res) -> None:
        self.resolution_x, self.resolution_y = res

    def notify(self) -> None:
        for subject in self._registered_subjects:
            subject.update()

    def update_attr(self, name: str, value: Any):
        setattr(self, name, value)
        self.notify()

    @classmethod
    def get_default_config(cls) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read_dict(cls._default_config)
        return config
