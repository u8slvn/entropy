from __future__ import annotations

import glob
import importlib
import os

from typing import Type

from entropy.game.states.base import State


_states: dict[str, Type[State]] = {}


def load():
    global _states

    pwd = os.path.dirname(__file__)
    entries = glob.glob(os.path.join(pwd, "*"))
    for entry in entries:
        if entry.startswith("__"):
            continue

        entry = os.path.basename(entry).replace(".py", "")
        importlib.import_module(f"{__name__}.{entry}")

    _states = State.get_states()


def get(state: str) -> Type[State]:
    try:
        return _states[state]
    except KeyError:
        raise Exception(f"State {state} does not exist.")
