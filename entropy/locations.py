from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parent
USER_HOME = Path.home()

ASSETS_DIR = ROOT.joinpath("assets")
LOCALES_DIR = ROOT.joinpath("locales")

CONFIG_PATH = USER_HOME.joinpath(".entropy")
