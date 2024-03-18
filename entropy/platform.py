from __future__ import annotations

import os
import sys

from pathlib import Path


WIN = sys.platform.startswith("win")

APPDATA = os.getenv("APPDATA")


def configure() -> None:
    """Configure platform related needs."""
    if WIN:
        # Make pygame high DPI aware
        import ctypes

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()


def get_user_local_storage() -> Path:
    """Return the user local storage path. Used to store user saves and config."""
    if WIN and APPDATA is not None:
        appdata = Path(APPDATA)
        return appdata.parent.joinpath("LocalLow/entropy")

    return Path.home().joinpath("entropy")
