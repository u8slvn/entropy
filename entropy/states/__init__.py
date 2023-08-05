from __future__ import annotations

import glob
import importlib
import os

from typing import Type

from entropy.states.base import State


_states: dict[str, Type[State]] = {}


def load():
    global _states

    pwd = os.path.dirname(__file__)
    files = glob.glob(os.path.join(pwd, "*.py"))
    module_names = [os.path.basename(f)[:-3] for f in files if "__" not in f]
    for module_name in module_names:
        importlib.import_module(f"{__name__}.{module_name}")

    _states = State.get_states()


def get(state: str) -> Type[State]:
    try:
        return _states[state]
    except KeyError:
        raise Exception(f"State {state} does not exist.")
