from __future__ import annotations

from pathlib import Path

from entropy import platform
from entropy.logging import get_logger


logger = get_logger()

ROOT = Path(__file__).parent
logger.debug(f"Root dir: {ROOT}")

ASSETS_DIR = ROOT.joinpath("assets")
logger.debug(f"Assets dir: {ROOT}")
LOCALES_DIR = ROOT.joinpath("locales")
logger.debug(f"Locales dir: {ROOT}")
STORY_DIR = ROOT.joinpath("story")
logger.debug(f"Story dir: {ROOT}")

USER_LOCAL_DIR = platform.get_user_local_storage()
logger.debug(f"User local dir: {USER_LOCAL_DIR}")
CONFIG_FILE_PATH = USER_LOCAL_DIR.joinpath("config.cfg")
logger.debug(f"Config file path: {CONFIG_FILE_PATH}")
