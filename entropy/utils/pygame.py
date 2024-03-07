from __future__ import annotations

import functools

from typing import Any
from typing import Callable
from typing import TypeVar

import pygame as pg


FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def reset_display(func: FuncT) -> FuncT:
    """
    Avoid crash between switch mode when `pygame.display.set_mode` is called with
    `SCALED` flag after being initialized without it.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        pg.display.quit()
        pg.display.init()
        return func(*args, **kwargs)

    return wrapper
