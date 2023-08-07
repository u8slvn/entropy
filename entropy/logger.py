from __future__ import annotations

import logging


def configure():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s - %(message)s",
    )
