from __future__ import annotations

import os
import sys


WIN = sys.platform.startswith("win")


def configure_display():
    """Configure display."""

    # Center window
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    if WIN is True:
        # Make pygame high DPI aware
        import ctypes

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
