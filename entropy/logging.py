from __future__ import annotations

import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
)


def logger():
    return logging.getLogger("entropy")
