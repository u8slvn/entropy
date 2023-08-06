from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path
from typing import Any

from entropy.tools.observer import Observer


class Config(Observer):
    _default_config = OrderedDict(
        {
            "display": OrderedDict(
                {
                    "fps": 60,
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
        self.fullscreen = config.getboolean("display", "fullscreen")
        self.lang = config.get("locale", "lang")

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
