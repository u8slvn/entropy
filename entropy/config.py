from __future__ import annotations

import configparser

from collections import OrderedDict
from pathlib import Path


class Config:
    _default_config = OrderedDict(
        {
            "display": OrderedDict(
                {
                    "fps": 60,
                    "fullscreen": False,
                }
            )
        }
    )

    def __init__(self, config_file: Path | None = None) -> None:
        config = self.get_default_config()

        if config_file is not None:
            config.read(config_file)

        self.fps = config.getfloat("display", "fps")
        self.fullscreen = config.getboolean("display", "fullscreen")

    @classmethod
    def get_default_config(cls) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read_dict(cls._default_config)
        return config
