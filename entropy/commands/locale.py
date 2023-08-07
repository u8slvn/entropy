from __future__ import annotations

from entropy import config
from entropy import translator
from entropy.commands.base import Command


class SwitchLocaleTo(Command):
    def __init__(self, locale: str):
        self._locale = locale

    def __call__(self) -> None:
        if translator.locale == self._locale:
            return

        translator.set_translation(locale=self._locale)
        config.update_attr(name="locale", value=self._locale)
